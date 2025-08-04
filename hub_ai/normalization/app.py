import logging
import os
import shutil
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from datetime import datetime
import sys
#parent changed
from pathlib import Path
# Get the current directory and normalization path
current_dir = Path(__file__).parent
normalization_dir = current_dir 
#  Change to normalization directory to maintain existing imports
os.chdir(normalization_dir)
# Add normalization directory to Python path
sys.path.insert(0, str(normalization_dir))

import normalise.env as env
from normalise.src.common.logging_config import setup_logging
from normalise.src.normalization.normalizer import Normalizer
from normalise.src.common.data_io import save_dataframe
from normalise.src.common.s3_utils import check_and_download_file, check_and_download_file_from_uri
from normalise.src.common.snowflake_utils import upload_df_to_snowflake
from normalise.src.normalization.benchmarking import Benchmarker
from normalise.src.common.pg_db_utils import PostgresConnector

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)
import json


app = FastAPI()

class NormalizeRequest(BaseModel):
    workspace_id: str
    folder_id: str
    custom_name: str

class BenchmarkRequest(BaseModel):
    workspace_id: str
    s3_path: str
    url: str

LOGGER: Optional[logging.Logger] = None


@app.on_event("startup")
def startup_event():
    global LOGGER
    try:
        LOGGER = setup_logging()
    except Exception as e:
        LOGGER = logging.getLogger("startup_failure")
        logging.basicConfig(level=logging.ERROR)
        LOGGER.error(f"FATAL: Could not initialize application. Error: {e}", exc_info=True)

def run_normalization_job(
    workspace_id: str, 
    folder_id: str,
    S3_INPUT_BUCKET: str, 
    custom_name: str,
    secret_name, 
    region_name,
    material_description: str = None,
):
    logger = setup_logging()
    logger.info("Received payload for normalization job:")
    logger.info(f"  workspace_id: {workspace_id}")
    logger.info(f"  folder_id: {folder_id}")
    logger.info(f"  custom_name: '{custom_name}'")
    logger.info(f"  S3_INPUT_BUCKET: {S3_INPUT_BUCKET}")
    logger.info(f"  secret_name: {secret_name}")
    logger.info(f"  region_name: {region_name}")
    logger.info(f"  material_description: {material_description}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_run_dir = os.path.join(env.BASE_TEMP_DIR, f"{workspace_id}_{timestamp}")
    os.makedirs(temp_run_dir, exist_ok=True)

    pg = PostgresConnector(logger)
    pg.connect()
    table_name = '"idp-meta-data"'
    where_clause = f"workspace_id = '{workspace_id}' AND custom_name = '{custom_name}' AND is_normalization = TRUE"

    logger.info(f"Starting normalization job for workspace '{workspace_id}' with folder_id '{folder_id}'")

    try:
        # Only update status if material_description is NOT provided
        if not material_description:
            try:
                logger.info(f"Updating status to 'Normalization-In Progress' for table {table_name} where {where_clause}")
                pg.mark_status(table_name, where_clause, status="Normalization-In Progress")

                verify_query = f"SELECT status FROM {table_name} WHERE {where_clause}"
                result = pg.execute_query(verify_query)
                if not result or result[0].get("status") != "Normalization-In Progress":
                    raise RuntimeError("Status verification failed. Status is not set to 'Normalization-In Progress'.")
                logger.info("Status update confirmed: 'Normalization-In Progress' successfully set in the database.")
            except Exception as status_err:
                logger.warning(f"Failed to update or verify status to 'Normalization-In Progress': {status_err}")
                raise

        # Run normalization logic for both cases
        if material_description:
            logger.info(f"Running normalization based on material_description: {material_description}")
            normalizer = Normalizer(logger)
            normalized_df = normalizer.run(material_description=material_description)
        else:
            env.S3_INPUT_BUCKET = S3_INPUT_BUCKET
            if not env.S3_INPUT_BUCKET:
                raise RuntimeError("S3_INPUT_BUCKET is not set in environment/config.")
            input_file_path, row_count = check_and_download_file(env.S3_INPUT_BUCKET, folder_id, temp_run_dir, logger)
            total_time_taken_mins = (row_count / 3) / 60
            logger.info(f"Input file successfully downloaded to: {input_file_path}")
            
            try:

                logger.info(f"Updating status to 'Normalization-In Progress' for table {table_name} where {where_clause}")
                pg.mark_status(table_name, where_clause, status=f"Normalization-In Progress, ETA : {total_time_taken_mins:.2f} minutes")

                verify_query = f"SELECT status FROM {table_name} WHERE {where_clause}"
                result = pg.execute_query(verify_query)

                if not result or "Normalization-In Progress" not in result[0].get("status", ""):
                    raise RuntimeError("Status verification failed. Status is not set to 'Normalization-In Progress'.")
                logger.info("Status update confirmed: 'Normalization-In Progress' successfully set in the database.")
            except Exception as status_err:
                logger.warning(f"Failed to update or verify status to 'Normalization-In Progress': {status_err}")
                raise
            
            normalizer = Normalizer(logger)
            normalized_df = normalizer.run(input_df_path=input_file_path)

        normalized_df['custom_name'] = custom_name
        if normalized_df.empty:
            logger.warning("Normalization resulted in an empty DataFrame. Aborting upload to Snowflake.")
            return

        #columnn rename from B2B Query to B2B_QUERY AND Cluster_ID to CLUSTER_ID
        index_cols = [col for col in normalized_df.columns if col.lower().startswith('_original_index')]
        normalized_df.drop(columns=index_cols, inplace=True, errors='ignore')
        normalized_df.rename(columns={'B2B Query': 'B2B_QUERY', 'Cluster_ID': 'CLUSTER_ID', 'description': 'Item Description'}, inplace=True)

        columns_to_keep = ['RESPONSE'] + ['B2B_QUERY'] + ['custom_name'] + ['CLUSTER_ID'] + ['Item Description']
        exclude_cols = set( ['custom_name', 'CLUSTER_ID', 'RESPONSE'])
        original_input_columns = [col for col in normalized_df.columns if col not in exclude_cols]

        normalized_df['RESPONSE'] = normalized_df[original_input_columns].apply(
                                    lambda row: json.dumps(row.to_dict(), ensure_ascii=False), axis=1
                                    )
        normalized_df = normalized_df.loc[:, [col for col in columns_to_keep if col in normalized_df.columns]]

        logger.info(f"Normalization complete. {len(normalized_df)} records processed.")
        snowflake_table_name = "NORMALISED_DATA"
        logger.info(f"Attempting to upload results to Snowflake table: {snowflake_table_name}")
        upload_df_to_snowflake(
            normalized_df,
            snowflake_table_name,
            workspace_id,
            logger,
            region_name
        )
        logger.info("Successfully uploaded data to Snowflake.")

        # Only update status if material_description is NOT provided
        if not material_description:
            try:
                logger.info(f"Updating status to ENDED for table {table_name} where {where_clause}")
                pg.mark_status(table_name, where_clause, status="Completed")
            except Exception as status_err:
                logger.warning(f"Failed to update status to ENDED: {status_err}")

    except Exception as e:
        logger.error(f"Job failed for workspace '{workspace_id}'. Error: {e}", exc_info=True)

        # Only update status if material_description is NOT provided
        if not material_description:
            try:
                logger.info(f"Updating status to FAILED for table {table_name} where {where_clause}")
                pg.mark_status(table_name, where_clause, status="Normalization-Failed")
            except Exception as status_err:
                logger.warning(f"Failed to update status to FAILED: {status_err}")

    finally:
        shutil.rmtree(temp_run_dir)

def run_benchmarking_job(workspace_id: str, s3_path: str, url: str):
    logger = setup_logging()
    temp_run_dir = os.path.join(env.BASE_TEMP_DIR, f"benchmark_{workspace_id}")
    os.makedirs(temp_run_dir, exist_ok=True)

    pg = PostgresConnector(logger)
    pg.connect()

    try:
        table_name = '"benchmarking_findings"'
        where_clause = f"workspace_id = '{workspace_id}'"

        try:
            logger.info(f"Updating status to IN_PROGRESS for table {table_name} where {where_clause}")
            pg.mark_status_inprogress(table_name, where_clause)
        except Exception as status_err:
            logger.warning(f"Failed to update status to IN_PROGRESS: {status_err}")

        benchmarker = Benchmarker(logger)
        benchmark_df = benchmarker.run(workspace_id, s3_path, url)

        if benchmark_df.empty:
            logger.warning("Benchmarking resulted in an empty DataFrame.")
            return

        logger.info(f"Benchmarking complete. {len(benchmark_df)} records processed.")

        try:
            logger.info(f"Updating status to ENDED for table {table_name} where {where_clause}")
            pg.mark_status_ended(table_name, where_clause)
        except Exception as status_err:
            logger.warning(f"Failed to update status to ENDED: {status_err}")

    except Exception as e:
        logger.error(f"Benchmarking job failed for workspace '{workspace_id}'. Error: {e}", exc_info=True)

    finally:
        logger.info(f"Benchmarking job finished for workspace '{workspace_id}'.")

# @app.post("/normalize", status_code=201)
# async def trigger_normalization(
#     request: NormalizeRequest,
#     background_tasks: BackgroundTasks 
# ):

#     if not env.S3_INPUT_BUCKET:
#         raise HTTPException(status_code=500, detail="S3_INPUT_BUCKET is not set in environment/config.")
#     temp_check_dir = "./data/temp/check/"
#     os.makedirs(temp_check_dir, exist_ok=True)
#     try:
#         input_file_path = check_and_download_file(env.S3_INPUT_BUCKET, request.folder_id, temp_check_dir, LOGGER)
#         if os.path.exists(input_file_path):
#             os.remove(input_file_path)
#     except FileNotFoundError:
#         LOGGER.warning(f"Requested S3 key '{request.folder_id}' not found. Not starting background job.")
#         raise HTTPException(status_code=404, detail=f"File or folder '{request.folder_id}' not found in S3 bucket.")
#     except Exception as e:
#         LOGGER.error("Error during S3 existence check, Error")
#         raise HTTPException(status_code=500, detail=str(e))
#     LOGGER.info(f"Received normalization request for workspace: '{request.workspace_id}', S3 key: '{request.folder_id}'")
#     background_tasks.add_task(
#         run_normalization_job,
#         workspace_id=request.workspace_id,
#         folder_id=request.folder_id,
#         custom_name=request.custom_name
#     )
#     return {
#         "status": "Accepted",
#         "message": "Normalization job has been queued and will be processed in the background.",
#         "workspace_id": request.workspace_id,
#         "s3_folder_id": request.folder_id
#     }

# @app.post("/benchmark", status_code=202)
# async def trigger_benchmark(
#     request: BenchmarkRequest,
#     background_tasks: BackgroundTasks
# ):
#     if LOGGER is None:
#         raise HTTPException(status_code=500, detail="Server is not properly configured.")
#     LOGGER.info(f"Received benchmarking request for workspace: '{request.workspace_id}', S3 path: '{request.s3_path}'")
#     temp_check_dir = "./data/temp/check/"
#     os.makedirs(temp_check_dir, exist_ok=True)
#     try:
#         input_file_path = check_and_download_file_from_uri(request.s3_path, temp_check_dir, LOGGER)
#         if os.path.isfile(input_file_path):
#             os.remove(input_file_path)
#     except FileNotFoundError:
#         LOGGER.warning(f"Requested S3 key '{request.s3_path}' not found. Not starting background job.")
#         raise HTTPException(status_code=404, detail=f"File or folder '{request.s3_path}' not found in S3 bucket.")
#     except Exception as e:
#         LOGGER.error(f"Error during S3 existence check: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
#     background_tasks.add_task(
#         run_benchmarking_job,
#         workspace_id=request.workspace_id,
#         s3_path=request.s3_path,
#         url=request.url
#     )
#     return {
#         "status": "Accepted",
#         "message": "Benchmarking job has been queued and will be processed in the background.",
#         "workspace_id": request.workspace_id,
#         "s3_path": request.s3_path
#     }

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)