"""Module contains common functions leveraging the PG connector object to perform db operations"""

import json

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

log = get_logger("pg_operations")


def get_content_from_db(tenant_id: str, document_id: int) -> pd.DataFrame:
    """
    Retrieve content from a PostgreSQL database and store it as a DataFrame.

    Args:
        tenant_id (str): Unique identifier for tenant
        document_id (int): The document id to fetch document chunk for

    Returns:
        pd.DataFrame: A pandas dataframe for document chunks
    """
    pg_db_conn = PGConnector(tenant_id=tenant_id)

    query_data = pg_db_conn.select_document_chunks(doc_id=document_id)

    columns = ["chunk_id", "document_id", "chunk_content", "page", "embedding"]
    df_query = pd.DataFrame(query_data, columns=columns)
    df_query["embedding"] = df_query["embedding"].map(json.loads)
    log.info("Loaded document chunks.")
    pg_db_conn.close_connection()

    return df_query


# TODO: Remove the function once get_content_from_db is updated to accept doc_id list
def get_content_for_doc_list_from_db(
    tenant_id: str,
    doc_ids: list[int],
    columns: list[str],
) -> pd.DataFrame:
    """
    Retrieve content from the PostgreSQL database as a DataFrame.
    Process the 'embedding' column in the given DataFrame if available.

    Args:
        doc_ids (List[int]): List of document ids
        columns (List[str]): List of required columns

    Returns:
        pd.DataFrame: A pandas dataframe for document chunks
    """
    pg_db_conn = PGConnector(tenant_id=tenant_id)

    query_data = pg_db_conn.select_document_chunks_from_doc_list(doc_ids=doc_ids)
    df_query = pd.DataFrame(query_data, columns=columns)
    if "embedding" in columns:
        df_query["embedding"] = df_query["embedding"].map(json.loads)
    log.info("Loaded document chunks.")
    pg_db_conn.close_connection()

    return df_query


@log_time
def get_content_by_document_type_from_db(
    tenant_id: str,
    document_type: str,
    columns: list[str],
) -> pd.DataFrame:
    """
    Retrieve content by document type from the PostgreSQL database as a DataFrame.
    Process the 'embedding' column in the given DataFrame if available.

    Args:
        document_type (str): Fetch the list of documents based on this document_type
        columns (List[str]): List of columns required in the response pandas dataframe

    Returns:
        pd.DataFrame: A pandas dataframe for document chunks
    """
    pg_db_conn = PGConnector(tenant_id=tenant_id)

    query_data = pg_db_conn.select_document_type_summaries(document_type=document_type)
    df_query = pd.DataFrame(query_data, columns=columns)
    if "embedding" in columns or "summary_embedding" in columns:
        df_query["summary_embedding"] = df_query["summary_embedding"].map(json.loads)
    log.info("Loaded document chunks.")
    pg_db_conn.close_connection()

    return df_query


def get_news_data_for_specific_category_and_date(
    tenant_id: str,
    ksc_type: str,
    ksc_name: str,
    date_range=None,
) -> pd.DataFrame:
    """Retrieve news data for a specific category and date range.

    Args:
        category (str): The category to filter news data.
        date_range (Optional[Dict[str, str]]): A dictionary containing start_date and end_date.

    Returns:
        pd.DataFrame: DataFrame containing news data for the specified category and date range.
    """
    pg_db_conn = PGConnector(tenant_id=tenant_id)

    news_data = pg_db_conn.select_news_chunk_data(ksc_type, ksc_name, date_range)

    news_data = pd.DataFrame(
        news_data,
        columns=["news_id", "chunk_id", "chunk_content", "embeddings", "title", "link"],
    )
    news_data.dropna(subset=["embeddings"], inplace=True)
    news_data["embeddings"] = news_data["embeddings"].map(json.loads)
    return news_data


def get_list_of_ksc_names(tenant_id: str) -> tuple[list[str], list[str], list[str]]:
    """Retrieve list_of_KSC_names
    Args:
        tenant_id for which Keyword, supplier and category names are to be selected
    Returns:
        list[str]: A list of distinct KSC_name values.
    """
    pg_db_conn = PGConnector(tenant_id=tenant_id)

    ksc_data = pg_db_conn.select_list_of_ksc_names()

    suppliers = [name for name, source in ksc_data if source == "supplier"]
    categories = [name for name, source in ksc_data if source == "category"]
    keywords = [name for name, source in ksc_data if source == "keyword"]
    return suppliers, categories, keywords


def fuzzy_search_contract_content(user_questions, tenant_id: str) -> int | None:
    """
    Searches the content using psql fuzzy search to find any contract
      which has matching content for the user question

    Args:
        questions (list(str)): series of user questions

    Returns:
        any matching doc id
    """
    pg_db_conn = PGConnector(tenant_id=tenant_id)

    doc_id = pg_db_conn.search_contract_doc_content_user_query(user_questions)
    log.info(f"Matching contract is {doc_id}")
    pg_db_conn.close_connection()
    return doc_id
