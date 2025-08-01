import logging
import os
import shutil
from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from pydantic import BaseModel, Field
from omegaconf import OmegaConf, DictConfig
from typing import Optional
import uvicorn
from datetime import datetime

from src.common.logging_config import setup_logging
from src.normalization.normalizer import Normalizer
from src.common.data_io import save_dataframe
from src.common.s3_utils import check_and_download_file,check_and_download_file_from_uri
from src.common.snowflake_utils import upload_df_to_snowflake
from src.normalization.benchmarking import Benchmarker
from src.common.pg_db_utils import PostgresConnector


# --- Pydantic Model for the Request Body ---
class NormalizeRequest(BaseModel):
    workspace_id: str = Field(..., description="A unique identifier for the workspace")
    folder_id: str = Field(..., description="The S3 folder path (key) containing the input file.")
    custom_name: str= Field(..., description="Optional custom name for the output file. If not provided, defaults to 'normalized_data.csv'.")
class BenchmarkRequest(BaseModel):
    workspace_id: str = Field(..., description="A unique identifier for the workspace")
    s3_path: str = Field(..., description="The S3 folder path (key) containing the scraped data file.")
    url: str = Field(..., description="The source URL of the data.")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Async Generative AI Normalization Service",
    description="An API to trigger background normalization of procurement data from S3 to Snowflake.",
    version="2.1.0"
)

# Global config and logger placeholders
CONFIG: Optional[DictConfig] = None
LOGGER: Optional[logging.Logger] = None

# --- Application Startup Event ---
@app.on_event("startup")
def startup_event():
    """Load base configuration and setup logger on application startup."""
    global CONFIG, LOGGER
    try:
        default_cfg_path = "./configs/norm_default_config.yaml"
        if not os.path.exists(default_cfg_path):
            raise FileNotFoundError(f"Default config not found at {default_cfg_path}")
        
        config = OmegaConf.load(default_cfg_path)
        
        # Setup a generic logger for the API itself
        api_logger_config = config.copy()
        api_logger_config.client_name = "NormalizationAPI"
        LOGGER = setup_logging(api_logger_config)
        
        CONFIG = config
        LOGGER.info("FastAPI Normalization Service starting up. Configuration loaded.")

    except Exception as e:
        # Use a basic logger if setup fails
        LOGGER = logging.getLogger("startup_failure")
        logging.basicConfig(level=logging.ERROR)
        LOGGER.error(f"FATAL: Could not initialize application. Error: {e}", exc_info=True)
        CONFIG = None

# --- Core Background Task ---
def run_normalization_job(config: DictConfig, workspace_id: str, folder_id: str, custom_name: str):
    """
    This function runs in the background. It orchestrates the entire ETL process.
    1. Sets up run-specific logging.
    2. Downloads data from S3.
    3. Runs the normalization logic.
    4. Uploads the result to Snowflake.
    5. Cleans up local files.
    """
    # 1. Setup run-specific logger using the workspace_id for uniqueness
    run_config = config.copy()
    run_config.client_name = workspace_id  # Use workspace_id for the log file name
    logger = setup_logging(run_config)
    logger.info(f"Background job started for workspace '{workspace_id}'.")

    # Create a temporary directory for this run's files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_run_dir = os.path.join(config.paths.base_temp_dir, f"{workspace_id}_{timestamp}")
    os.makedirs(temp_run_dir, exist_ok=True)

    # Create PostgresConnector instance
    pg = PostgresConnector(config, logger)
    pg.connect()

    try:
        # inn progress
        try:
            table_name = '"idp-meta-data"'
            where_clause = f"workspace_id = '{workspace_id}' AND custom_name = '{custom_name}'"
            pg.mark_status_inprogress(table_name, where_clause)
            logger.info(f"Marked status as 'in_progress' for workspace '{workspace_id}' with custom_name '{custom_name}'")
        except Exception as e:
            logger.error(f"Failed to mark status as 'in_progress' for workspace '{workspace_id}': {e}", exc_info=True)
        # 2. Download the appropriate file from S3
        logger.info(f"Searching for input file in S3 bucket '{config.s3.input_bucket}' within folder '{folder_id}'")
        input_file_path = check_and_download_file(run_config.s3.input_bucket, folder_id, temp_run_dir, logger)
        logger.info(f"Input file successfully downloaded to: {input_file_path}")

        # 3. Run the normalization process
        normalizer = Normalizer(run_config, logger)
        normalized_df = normalizer.run(input_df_path=input_file_path)
        normalized_df['custom_name'] = custom_name

        if normalized_df.empty:
            logger.warning("Normalization resulted in an empty DataFrame. Aborting upload to Snowflake.")
            return

        logger.info(f"Normalization complete. {len(normalized_df)} records processed.")

        # 4. Upload the result to Snowflake
        snowflake_table_name = "NORMALISED_DATA"
        logger.info(f"Attempting to upload results to Snowflake table: {snowflake_table_name}")

        upload_df_to_snowflake(
            df=normalized_df,
            table_name=snowflake_table_name,
            snowflake_config=run_config.snowflake,
            workspace_id=run_config.client_name,
            logger=logger
        )
        logger.info("Successfully uploaded data to Snowflake.")
        try:
            table_name = '"idp-meta-data"'
            where_clause = f"workspace_id = '{workspace_id}' AND custom_name = '{custom_name}'"
            pg.mark_status_ended(table_name, where_clause)
            logger.info(f"Marked status as 'ended' for workspace '{workspace_id}' with custom_name '{custom_name}'")
        except Exception as e:
            logger.error(f"Failed to mark status as 'endded' for workspace '{workspace_id}': {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Job failed for workspace '{workspace_id}'. Error: {e}", exc_info=True)


        # 5. Cleanup
        shutil.rmtree(temp_run_dir)
        logger.info(f"Cleaned up temporary directory: {temp_run_dir}")
        logger.info(f"Background job finished for workspace '{workspace_id}'.")

# --- Core Background Task for Benchmarking ---
def run_benchmarking_job(config: DictConfig, workspace_id: str, s3_path: str, url: str):
    run_config = config.copy()
    run_config.client_name = workspace_id
    logger = setup_logging(run_config)
    logger.info(f"Benchmarking job started for workspace '{workspace_id}'.")
    temp_run_dir = os.path.join(config.paths.base_temp_dir, f"benchmark_{workspace_id}")
    os.makedirs(temp_run_dir, exist_ok=True)
    # Create PostgresConnector instance
    pg = PostgresConnector(config, logger)
    pg.connect()
    try:
        try:
            table_name = '"benchmarking_findings"'
            where_clause = f"workspace_id = '{workspace_id}'"
            pg.mark_status_inprogress(table_name, where_clause)
            logger.info(f"Marked status as 'in_progress' for workspace '{workspace_id}'")
        except Exception as e:
            logger.error(f"Failed to mark status as 'in_progress' for workspace '{workspace_id}': {e}", exc_info=True)
        benchmarker = Benchmarker(run_config, logger)
        benchmark_df = benchmarker.run(workspace_id, s3_path, url)
        if benchmark_df.empty:
            logger.warning("Benchmarking resulted in an empty DataFrame.")
            return
        logger.info(f"Benchmarking complete. {len(benchmark_df)} records processed.")
        # Note: Snowflake upload is handled inside Benchmarker.run() method
        try:
            table_name = '"benchmarking_findings"'
            where_clause = f"workspace_id = '{workspace_id}'"
            pg.mark_status_ended(table_name, where_clause)
            logger.info(f"Marked status as 'ended' for workspace '{workspace_id}'")
        except Exception as e:
            logger.error(f"Failed to mark status as 'ended' for workspace '{workspace_id}': {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Benchmarking job failed for workspace '{workspace_id}'. Error: {e}", exc_info=True)
    finally:
        logger.info(f"Benchmarking job finished for workspace '{workspace_id}'.")

# --- Normalization API Endpoint ---
@app.post("/normalize", status_code=201)
async def trigger_normalization(
    request: NormalizeRequest,
    background_tasks: BackgroundTasks 
):
    """
    Accepts a folder ID or file name, verifies it in S3, and triggers a long-running
    normalization process in the background. Responds immediately with status 'Accepted' only if file exists.
    """

    if CONFIG is None or LOGGER is None:
        raise HTTPException(status_code=500, detail="Server is not properly configured.")
    
    # Check if the file/folder exists in S3 before starting the background task
    temp_check_dir = "./data/temp/check/"
    os.makedirs(temp_check_dir, exist_ok=True)
    try:
        input_file_path = check_and_download_file(CONFIG.s3.input_bucket, request.folder_id, temp_check_dir, LOGGER)
        # Clean up the check file after confirming existence
        if os.path.exists(input_file_path):
            os.remove(input_file_path)  #add an entry new 
    except FileNotFoundError:
        LOGGER.warning(f"Requested S3 key '{request.folder_id}' not found. Not starting background job.")
        raise HTTPException(status_code=404, detail=f"File or folder '{request.folder_id}' not found in S3 bucket.")
    except Exception as e:
        LOGGER.error("Error during S3 existence check, Error")
        raise HTTPException(status_code=500, detail=str(e))

    LOGGER.info(f"Received normalization request for workspace: '{request.workspace_id}', S3 key: '{request.folder_id}'")
    
    # Check if the file/folder exists in S3 before starting the background task
    temp_check_dir = "./data/temp/check/"
    os.makedirs(temp_check_dir, exist_ok=True)
    try:
        # This will raise FileNotFoundError if not found
        input_file_path = check_and_download_file(CONFIG.s3.input_bucket, request.folder_id, temp_check_dir, LOGGER)
        # Clean up the check file after confirming existence
        if os.path.isfile(input_file_path):
            os.remove(input_file_path)
    except FileNotFoundError:
        LOGGER.warning(f"Requested S3 key '{request.folder_id}' not found. Not starting background job.")
        raise HTTPException(status_code=404, detail=f"File or folder '{request.folder_id}' not found in S3 bucket.")
    except Exception as e:
        LOGGER.error(f"Error during S3 existence check: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        #end base on the custom_name and workspace_id 
    # If we reach here, file exists, so queue the background job
    background_tasks.add_task(
        run_normalization_job,
        config=CONFIG,
        workspace_id=request.workspace_id,
        folder_id=request.folder_id,
        custom_name=request.custom_name
    )
    return {
        "status": "Accepted",
        "message": "Normalization job has been queued and will be processed in the background.",
        "workspace_id": request.workspace_id,
        "s3_folder_id": request.folder_id
    }

@app.post("/benchmark", status_code=202)
async def trigger_benchmark(
    request: BenchmarkRequest,
    background_tasks: BackgroundTasks
):
    if CONFIG is None or LOGGER is None:
        raise HTTPException(status_code=500, detail="Server is not properly configured.")
    LOGGER.info(f"Received benchmarking request for workspace: '{request.workspace_id}', S3 path: '{request.s3_path}'")
    temp_check_dir = "./data/temp/check/"
    os.makedirs(temp_check_dir, exist_ok=True)
    try:
        LOGGER.info(f"Type of CONFIG.s3.benchmark_input_bucket: {type(CONFIG.s3.benchmark_input_bucket)}; value: {CONFIG.s3.benchmark_input_bucket}")
        
        input_file_path = check_and_download_file_from_uri(request.s3_path, temp_check_dir, LOGGER)
        if os.path.isfile(input_file_path):
            os.remove(input_file_path)
    except FileNotFoundError:
        LOGGER.warning(f"Requested S3 key '{request.s3_path}' not found. Not starting background job.")
        raise HTTPException(status_code=404, detail=f"File or folder '{request.s3_path}' not found in S3 bucket.")
    except Exception as e:
        LOGGER.error(f"Error during S3 existence check: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    background_tasks.add_task(
        run_benchmarking_job,
        config=CONFIG,
        workspace_id=request.workspace_id,
        s3_path=request.s3_path,
        url=request.url
    )
    return {
        "status": "Accepted",
        "message": "Benchmarking job has been queued and will be processed in the background.",
        "workspace_id": request.workspace_id,
        "s3_path": request.s3_path
    }

# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

def handle_normalization_request(s3_config, file_name, local_dir, logger, start_background_task):
    try:
        # Try to download the file by name
        local_file_path = check_and_download_file(s3_config, file_name, local_dir, logger)
        # If successful, start the background task
        start_background_task(local_file_path)
        logger.info(f"Background task started for file: {local_file_path}")
        return {"status": "accepted", "message": "Background task started."}
    except FileNotFoundError:
        logger.warning(f"Requested file '{file_name}' not found in S3.")
        return {"status": "not_found", "message": f"File '{file_name}' not found."}
    except Exception as e:
        logger.error(f"Error handling file request: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)