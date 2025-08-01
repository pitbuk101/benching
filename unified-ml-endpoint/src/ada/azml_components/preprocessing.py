"""Preprocessing functions to prepare data for the use cases."""

import concurrent.futures
import json
import os
import pathlib
import sys
import time

import mlflow
import pandas as pd

# flake8: noqa: E402
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from ada.components.db.pg_connector import PGConnector
from ada.use_cases.benchmarking.benchmarking import run_benchmarking
from ada.use_cases.clauses.clauses import run_clauses
from ada.use_cases.entity_extraction.entity_extraction import run_entity_extraction
from ada.use_cases.leakage.leakage import run_leakage
from ada.use_cases.pdf_reader.pdf_reader import run_pdf_reader
from ada.use_cases.summary.summary_generator import run_summary_generator
# from ada.utils.authorization.credentials import get_workspace_client_secret_credential
from ada.utils.azml.azml_utils import (
    azure_download_pdf,
    get_valid_secrets,
    pop_excess_environment_variables,
    set_openai_api_creds,
)
from ada.utils.config.config_loader import read_config, set_component_args
from ada.utils.io.misc import get_storage_details
from ada.utils.logs.logger import get_logger

log = get_logger("preprocessing")
conf = read_config("azml_deployment.yaml")
preprocessing_conf = read_config("use-cases.yml")["preprocessing"]
secrets_conf = read_config("secrets.yml")
global_conf = conf["global"]
pop_excess_environment_variables()


class MissingRequiredArgsException(Exception):
    """Raised when required arguments are missing"""


def run_functions_in_parallel(func_arg_lists) -> dict:
    """
    Execute multiple functions in parallel using a ProcessPoolExecutor.

    Args:
    func_arg_lists (list): A list of tuples/lists containing function references and
                           their arguments. Each element of the list should be in
                           the format (func, *args).

    Returns:
    - dict: A dict containing the return values of the executed functions.
    """

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = {func.__name__: executor.submit(func, *args) for func, *args in func_arg_lists}

    get_component_output = {}  # List to store the returned values

    for future_function in concurrent.futures.as_completed(results.values()):
        result = future_function.result()
        function_name = [name for name, future in results.items() if future == future_function][0]
        get_component_output[function_name] = result  # Store result with function name as key

    return get_component_output


def call_nodes(
    args,
    df_doc_chunks: pd.DataFrame,
    df_doc_info: pd.DataFrame,
    df_doc_tables: list[pd.DataFrame],
) -> dict:
    """
    Orchestrates the execution of nodes in parallel.

    Args:
        args: Arguments used in the preprocessing functions.
        df_doc_chunks (DataFrame): DataFrame containing document chunks.
        df_doc_info (DataFrame): DataFrame containing document information.
        df_doc_tables (list(DataFrame)): list of DataFrames representing tables extracted.
                                        Each DataFrame corresponds to one table in the document.

    Returns:
        dict: A dictionary containing output DataFrames from different preprocessing tasks:
            - "document_info_df": DataFrame with collected document information.
            - "document_chunks_df": Original document chunks DataFrame.
            - "summary_chunk_df": DataFrame containing summarized document chunks.
            - "leakage_df": DataFrame containing Leakage information

    The function starts the logging process, initializes a vector store,
    sets argument lists for each function, executes multiple preprocessing
    functions in parallel, collects results, and constructs output DataFrames
    containing the processed information.
    """
    # Start Logging
    start = time.time()

    log.info("Create vectorstore")

    log.info("Set argument list for each function")
    get_summary = [run_summary_generator, args.document_type, df_doc_chunks, args.tenant_id]
    get_entity_extraction = [run_entity_extraction, df_doc_chunks, args.tenant_id]
    get_benchmarking = [run_benchmarking, df_doc_chunks, args.tenant_id]
    get_clauses = [run_clauses, df_doc_chunks, args.tenant_id]
    get_leakage = [
        run_leakage,
        args.document_id,
        args.document_type,
        json.loads(args.sku_list),
        df_doc_tables,
        df_doc_chunks,
        args.tenant_id,
    ]

    log.info("Running summary, entity_extraction, benchmarking, clauses, leakage in parallel")
    function_argument_lists = [
        get_summary,
        get_entity_extraction,
        get_benchmarking,
        get_clauses,
        get_leakage,
    ]
    component_outputs = run_functions_in_parallel(function_argument_lists)
    log.info("All components executed")

    summary_result = component_outputs["run_summary_generator"][0]
    summary_embeddings = component_outputs["run_summary_generator"][1]
    clauses_result = component_outputs["run_clauses"]
    entity_extraction_result = component_outputs["run_entity_extraction"]
    benchmarking_result = component_outputs["run_benchmarking"]
    leakage_result = component_outputs["run_leakage"]

    end = time.time()
    log.info("It took %d", end - start)

    # Stop Logging
    mlflow.end_run()

    df_doc_info["summary"] = summary_result
    df_doc_info["summary_embedding"] = [summary_embeddings] * len(df_doc_info)

    df_contracts_kpi = pd.DataFrame(
        {
            "document_id": [args.document_id],
            "region": [args.region],
            "supplier": [args.supplier],
            "sku": [args.sku_list],
            "clauses": [json.dumps(clauses_result)],
            "benchmarking": [json.dumps(benchmarking_result)],
            "entity_extraction": [json.dumps(entity_extraction_result)],
        },
    )

    output_dfs = {
        "document_info_df": df_doc_info,
        "document_chunks_df": df_doc_chunks,
        "contracts_kpi_df": df_contracts_kpi,
        "leakage_df": leakage_result,
    }

    log.info("Preprocessing nodes executed successfully")

    return output_dfs


# pylint: disable=fixme
# TODO: implement error handling
def db_write(output_columns: dict, pg_conn, args) -> None:
    """
    Perform upsert operations to write data into specified database tables.

    Args:
        output_columns (dict): A dictionary containing DataFrames to be written to the database.
        pg_conn: An object representing the database connection.
        args: Parsed arguments passed to the function.

    Raises:
        Any exceptions that might occur during the upsert operation.

    This function executes upsert operations to write data into specific tables in the database.
    The upsert operations are performed based on the provided 'document_id' value as the key column.
    """
    log.info("run upsert to db")

    document_id = int(args.document_id)
    key_col_value_map = {"document_id": [document_id]}
    pg_conn.upsert_records(
        table_name=args.doc_info_table,
        data=output_columns["document_info_df"],
        key_col_value_map=key_col_value_map,
    )

    if args.document_type.lower() == "contract":
        pg_conn.upsert_records(
            table_name=args.contracts_kpi_table,
            data=output_columns["contracts_kpi_df"],
            key_col_value_map=key_col_value_map,
        )

    pg_conn.upsert_records(
        table_name=args.doc_chunks_table,
        data=output_columns["document_chunks_df"],
        key_col_value_map=key_col_value_map,
    )

    pg_conn.upsert_records(
        table_name=args.contract_sku_details_table,
        data=output_columns["leakage_df"],
        key_col_value_map=key_col_value_map,
    )

    log.info("preprocessing pipeline executed successfully")


def run_preprocessing_pipeline() -> None:
    """
    Runs a preprocessing pipeline to process PDF documents by performing various tasks:

    1. Reads configuration from 'azml_deployment.yaml' and retrieves secret names.
    2. Fetches global configuration and secret keys using Azure credentials.
    3. Sets OpenAI API credentials using the obtained secret keys.
    4. Retrieves arguments from a configuration file using set_component_args().
    5. Downloads a PDF document from an Azure blob storage container using Azure OCR credentials.
    6. Initiates a PostgreSQL Connector.
    7. Checks arguments and executes run_pdf_reader if all required arguments are available:
        - 'document_id', 'input_data_filename', 'document_type', 'region', 'category', 'supplier',
          'sku_list', 'embedding_model'.
    8. Calls run_pdf_reader function passing required arguments for PDF processing.
    9. Executes each method in the pipeline parallely using multiprocessing
    9. Writes output columns to a PostgreSQL database using db_write().

    If any of the required arguments are missing, it logs a message indicating that not all required
    arguments are set and the run_pdf_reader function cannot be executed.

    Returns:
        None
    """

    args = set_component_args()
    os.environ["AZURE_DATABASE_ACCESS"] = "1"
    os.environ["AZURE_CLIENT_SECRET"] = args.azure_client_secret
    os.environ["AZURE_CLIENT_SECRET_SECONDARY"] = args.azure_client_secret_secondary

    tenant_id = args.tenant_id
    (
        storage_account_name,
        storage_sp_key,
        storage_sp_key_secondary,
        client_id_key,
    ) = get_storage_details(
        global_conf["workspace_name"],
        tenant_id,
    )

    log.info("Storage details %s", storage_account_name)

    # Add storage account key and client id to secret_names dict(created dynamically)
    secret_names = {
        **secrets_conf,
        storage_sp_key: storage_sp_key,
        storage_sp_key_secondary: storage_sp_key_secondary,
        "client_id": client_id_key,
    }

    secret_keys = get_valid_secrets(
        secret_names=secret_names,
    )
    set_openai_api_creds(secret_keys=secret_keys)
    credential = get_workspace_client_secret_credential(
        tenant_id=global_conf["azure_tenant_id"],
        client_id=secret_keys["client_id"],
        primary_secret=secret_keys.get(storage_sp_key),
        secondary_secret=secret_keys.get(storage_sp_key_secondary),
    )

    # Read pdf document from blob
    azure_ocr_output = azure_download_pdf(
        storage_account_name=storage_account_name,
        credential=credential,
        filename=args.input_data_filename,
        container=args.input_container,
        vision_endpoint=secret_keys["vision_endpoint"],
        vision_key=secret_keys["vision_key"],
    )
    pg_connector = PGConnector(tenant_id=tenant_id)

    required_args = preprocessing_conf["mandatory_args"] + preprocessing_conf[
        "type_specific_args"
    ].get(args.document_type, [])
    log.info("Required args : %s", required_args)

    log.info("run pdf reader")

    if missing_required_args := [arg for arg in required_args if getattr(args, arg, None) is None]:
        error_message = (
            f"missing required arguments ({','.join(missing_required_args)}) "
            f"for document type {args.document_type}. Cannot execute run_pdf_reader."
        )
        log.error(error_message)
        raise MissingRequiredArgsException(error_message)
    df_doc_chunks, df_doc_info, df_doc_tables = run_pdf_reader(
        args.document_id,
        args.input_data_filename,
        args.document_type,
        args.category,
        azure_ocr_output,
        args.embedding_model,
    )
    output_columns = call_nodes(args, df_doc_chunks, df_doc_info, df_doc_tables)
    db_write(output_columns, pg_connector, args)


if __name__ == "__main__":
    log.info("preprocessing pipeline triggered")
    run_preprocessing_pipeline()
