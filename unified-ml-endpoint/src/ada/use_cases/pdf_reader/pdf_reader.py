"""PDF reader component for batch pipeline."""

import json

import numpy as np
import pandas as pd
# from azure.ai.formrecognizer import AnalyzeResult

# from ada.components.extractors.text_extractors import (
#     extract_tables_from_ocr_output,
#     split_text_into_pages,
# )
from ada.components.llm_models.chunks import create_chunks
from ada.components.llm_models.generic_calls import generate_embeddings_from_string
from ada.utils.azml.azml_utils import get_valid_secrets, set_openai_api_creds
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("pdf_reader")
conf = read_config("azml_deployment.yaml")
secrets_conf = read_config("secrets.yml")
model_confs = read_config("models.yml")
global_conf = conf["global"]

secret_names = {
    **secrets_conf,
}


def get_doc_info(
    document_id: int,
    input_data_filename: str,
    document_type: str,
    category: str,
    azure_ocr_output,
) -> pd.DataFrame:
    """
    Create pandas Dataframe with details related to uploaded documents

    Args:
        document_id (int): id of the received document
        input_data_filename (str): filename of the received document
        document_type (str): type of the received document
        category (str): selected category by the user
        azure_ocr_output: ocr output of the document from azure document analysis

    Returns:
        pd.DataFrame: Dataframe with One row with all details of the document
    """
    doc_info_columns = (
        "document_id",
        "document_name",
        "document_type",
        "category_name",
        "content",
    )
    doc_info_list = [
        (
            int(document_id),
            input_data_filename,
            document_type,
            category,
            str(json.dumps(azure_ocr_output.content)),
        ),
    ]
    return pd.DataFrame(doc_info_list, columns=list(doc_info_columns))


def get_doc_chunks(document_id: int, azure_ocr_output, embedding_model: str) -> pd.DataFrame:
    """
    This function takes OCR output and document ID as input and
    creates document chunks from OCR output.
    It also creates embeddings of those chunks and
    creates a pandas DataFrame with details like document ID,
    chunk ID, embedding, page number from Azure output, etc.

    Args:
        document_id (int): id of the received document
        azure_ocr_output: ocr output of the document from azure document analysis
        embedding_model (str): model name of the embedding

    Returns:
        pd.DataFrame: pandas Dataframe with doc chunks along with its embedding and other metadata
    """
    secret_keys = get_valid_secrets(
        secret_names=secret_names,
    )

    set_openai_api_creds(secret_keys=secret_keys)

    extracted_text = split_text_into_pages(azure_ocr_output)
    corpus = " ".join(list(extracted_text.values()))
    data_chunks = create_chunks(corpus)
    i = 1
    extracted_text_final = []
    for item in data_chunks:
        text_dict = {
            "chunk_id": i,
            "chunk_content": item.page_content,
            "page": item.metadata["source"],
        }
        content_embeddings = generate_embeddings_from_string(
            text_dict["chunk_content"],
            embedding_model,
        )
        text_dict["embedding"] = content_embeddings
        extracted_text_final.append(text_dict)
        i += 1
    doc_chunks_df = pd.DataFrame.from_records(extracted_text_final)
    doc_chunks_df["document_id"] = document_id

    doc_chunks_df["chunk_id"] = doc_chunks_df["chunk_id"].astype("int")
    doc_chunks_df["document_id"] = doc_chunks_df["document_id"].astype("int")
    doc_chunks_df["page"] = doc_chunks_df["page"].astype("int")
    doc_chunks_df["embedding"] = np.array(doc_chunks_df["embedding"])

    return doc_chunks_df


def get_doc_tables(azure_ocr_output: AnalyzeResult) -> list[pd.DataFrame]:
    """
    Extracts all table data from the OCR output and returns it as a list of dataframes.
    If a table is split into multiple tables, they are combined into one.

    Args:
        azure_ocr_output: ocr output of the document from azure document analysis

    Returns:
        list[pd.DataFrame]: List of pandas Dataframe where each dataframe represent one table
    """
    log.info(
        "Extracting tables from azure ocr output "
        "and creating a list of dataframe to store each table",
    )
    sanitized_tables: list[pd.DataFrame] = []
    extracted_tables = extract_tables_from_ocr_output(azure_ocr_output)
    for i, (_, table) in enumerate(extracted_tables):
        # Todo: Use of page number to increase the table join condition
        if any(
            isinstance(table[i][0], int) or (isinstance(table[i][0], str) and table[i][0].isdigit())
            for i in range(table.shape[1])
        ):
            try:
                table.columns = sanitized_tables[-1].columns
                sanitized_tables[-1] = pd.concat([sanitized_tables[-1], table]).reset_index(
                    drop=True,
                )
            except IndexError:
                log.error("Failed for the table with IndexError: %s", table)
            except ValueError:
                log.error("Failed for the table with ValueError: %s", table)
                sanitized_tables.append(
                    table.rename(columns=table.iloc[0]).drop(0).reset_index(drop=True),
                )

        else:
            sanitized_tables.append(
                table.rename(columns=table.iloc[0]).drop(0).reset_index(drop=True),
            )
    log.info("Number of tables %s ", len(sanitized_tables))
    return sanitized_tables


def run_pdf_reader(
    document_id: int,
    input_data_filename: str,
    document_type: str,
    category: str,
    azure_ocr_output,
    embedding_model: str,
) -> tuple[pd.DataFrame, pd.DataFrame, list[pd.DataFrame]]:
    """
    This function reads a PDF document, extracts relevant information
    and returns it in the form of dataframes.

    Parameters:
    document_id (int): The unique identifier for the document.
    input_data_filename (str): The name of the input data file.
    document_type (str): The type of the document.
    region (str): The region where the document was generated.
    category (str): The category of the document.
    azure_ocr_output: The output from Azure's OCR service.
    supplier (str): The supplier of the document.
    sku_list (str): The list of SKUs in the document in str format.
    embedding_model (str): The name of the embedding model used.

    Returns:
    doc_chunks_df (pd.DataFrame) : A dataframe containing chunks of the document.
    df_doc_info (pd.DataFrame) : A dataframe containing information about the document.
    df_doc_tables (list[pd.DataFrame]) : A list of dataframes containing tables in the document.
    """

    # TABLE 1 - Doc Info
    df_doc_info = get_doc_info(
        document_id,
        input_data_filename,
        document_type,
        category,
        azure_ocr_output,
    )

    # TABLE 2 - Doc Chunks
    doc_chunks_df = get_doc_chunks(document_id, azure_ocr_output, embedding_model)

    # LIST of TABLE - Doc Tables
    df_doc_tables = get_doc_tables(azure_ocr_output)

    return doc_chunks_df, df_doc_info, df_doc_tables
