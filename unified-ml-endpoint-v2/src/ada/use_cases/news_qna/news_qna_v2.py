"""News QnA use case."""

import json
import string
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
from fuzzywuzzy import fuzz
from langchain_core.documents import Document

from ada.components.db.pg_connector import PGConnector
from ada.components.db.pg_operations import (
    get_list_of_ksc_names,
    get_news_data_for_specific_category_and_date,
)
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    generate_qa_chain_response_with_sources,
)
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.news_qna.exception import NewsQnAException
from ada.use_cases.news_qna.prompts import (
    context_analyzation_prompt,
    news_qna_prompt,
    news_qna_prompt_list,
    query_analyzing_prompt,
)
from ada.utils.config.config_loader import read_config
from ada.utils.format.format import str_to_dict
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

log = get_logger("news_qna-v2")
news_conf = read_config("use-cases.yml")["news"]["context"]


@log_time
def run_news_qna(json_file_str: str) -> dict[str, Any]:
    """Run news qna processing to answer user question.

    Args:
        json_file_str (str): JSON string containing user query, category, and tenant ID.

    Returns:
        dict[str, Any]: Dictionary containing the response message and response type.
    """
    json_data: dict[str, Any] = json.loads(json_file_str)
    user_query = json_data.get("user_query", "")
    log.info("user question: %s", user_query)
    tenant_id = json_data["tenant_id"]
    dropdown_selected_category = json_data["category"]
    supplier_list, category_list, _ = get_list_of_ksc_names(tenant_id)

    extracted_query_type = extract_query_type(user_query)

    user_prompt = context_analyzation_prompt(user_query, category_list, supplier_list)

    extracted_entities = generate_chat_response_with_chain(user_prompt, model="gpt-4o")
    try:
        extracted_entities_dict = str_to_dict(extracted_entities)
    except json.JSONDecodeError as exc:
        log.error(
            "extracted_entities_dict isn't extracted in desired format from given user question",
        )
        raise NewsQnAException(
            "We encountered an issue while processing information, it will "
            "likely go away if you kindly ask the question again after a "
            "few seconds",
        ) from exc

    log.info("extracted entities from the user question is : %s", extracted_entities)
    extracted_mode = extracted_entities_dict.get("mode", "") if extracted_entities_dict else ""

    if extracted_mode == "listing":
        raise NewsQnAException(
            "Unfortunately we are currently developing the ability to list"
            " news articles or their summaries. "
            "query, please try requesting synthesis related questions. \n "
            "Note: The search was from the last 30 days of news, please specify "
            "timeframe.",
        )

    verified_ksc_name, extracted_type = get_ksc_name(
        extracted_entities_dict,
        supplier_list,
        category_list,
        dropdown_selected_category,
    )

    extracted_date_range = (
        extracted_entities_dict.get("date_range", []) if extracted_entities_dict else []
    )

    default_date_flag = False
    if extracted_date_range[0] == "NA":
        default_date_flag = True
        # current_date = datetime(2024, 2, 27)
        current_date = datetime.now()
        # reduce timedelta when we have latest data available
        start_date_str = (current_date - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date_str = current_date.strftime("%Y-%m-%d")
        extracted_date_range = [start_date_str, end_date_str]

    # work with final entities
    news_data = get_news_data(tenant_id, extracted_date_range, extracted_type, verified_ksc_name)
    log.info("news data dimension: %s", news_data.shape)
    if news_data.shape[0] == 0:
        raise NewsQnAException(
            "Unfortunately we couldn't retrieve any news articles for the selected "
            "query, please try another question. \n Note: The search was from the last "
            "90 days of news, please specify timeframe.",
        )

    answer, source_documents = get_news_answer(
        news_data,
        user_query,
        default_date_flag,
        mode=extracted_mode,
        query_type=extracted_query_type,
    )
    log.info("LLM response to user question: %s", answer)
    unique_sources = set()  # Set to store unique source IDs
    links = []
    for source in source_documents:
        source_id = source.metadata["source"]
        if source_id not in unique_sources:
            unique_sources.add(source_id)
            link_details = {
                "type": "news",
                "details": {
                    "title": source.metadata["title"],
                    "link": source.metadata["link"],
                },
            }
            links.append(link_details)
        if len(links) == news_conf["link_count"]:
            break

    return (
        {
            "message": answer.rstrip(string.punctuation.replace(".", " ")),
            "response_type": "summary",
            "links": links,
            "additional_text": "For more information, please visit below links .. ",
        }
        if links and len(links) > 0
        else {
            "message": answer.rstrip(string.punctuation.replace(".", " ")),
            "response_type": "summary",
        }
    )


def extract_query_type(user_query: str) -> str:
    """
    Analyzes user's query to determine its type.

    This function first analyzes the user query with `query_analyzing_prompt`, then uses
    `generate_chat_response` to generate a chat response. It tries to decode this response
    into a JSON object to extract 'query_type'. If decoding fails, indicating the response
    does not meet the expected format, a NewsQnAException is raised.

    Args:
        user_query (str): User's query.

    Returns:
        str: Extracted query type from the response.

    Raises:
        NewsQnAException: Raised if response cannot be decoded, indicating an unexpected
        format.

    Note:
    - `query_analyzing_prompt` analyzes and returns a prompt for further processing.
    - `generate_chat_response_with_chain` creates a response based on the generated prompt.
    - Errors caught as `json.JSONDecodeError` are logged before raising NewsQnAException,
    and the extracted query type is logged.
    """
    result_query_prompt = query_analyzing_prompt(user_query)
    result_query_prompt_generation = generate_chat_response_with_chain(result_query_prompt)

    try:
        result_query_prompt_generation_json = str_to_dict(result_query_prompt_generation)
    except json.JSONDecodeError as exc:
        log.error("extracted_query_type isn't extracted in desired format from given user question")
        raise NewsQnAException(
            "We encountered an issue while processing information, it will "
            "likely go away if you kindly ask the question again after a few seconds",
        ) from exc
    extracted_query_type = result_query_prompt_generation_json["query_type"]
    log.info("extracted_query_type is : %s", extracted_query_type)
    return extracted_query_type


def get_ksc_name(extracted_entities_dict, supplier_list, category_list, dropdown_selected_category):
    """
    Determines KSC_name (Keyword/Supplier/Category) from extracted user input entities.

    This function uses extracted entities, lists of known suppliers and categories, and the
    category selected from a dropdown to identify the KSC name. It checks the type of entity
    ('supplier', 'category', or 'keyword') and finds the highest similarity KSC name. Raises
    a NewsQnAException if the type is 'keyword', unrecognized, or no close match is found.

    Args:
        extracted_entities_dict (dict): Key info from the user query.
        supplier_list (list): Known suppliers.
        category_list (list): Known categories.
        dropdown_selected_category (str): User-selected category for 'none'.

    Returns:
        tuple: The verified KSC name and the extracted entity type.

    Raises:
        NewsQnAException: For no close match, 'keyword' type, or unrecognized type.

    Note:
    - `get_highest_similarity_ksc_name` finds the closest name in a list.
    - Verified KSC names are logged using `log.info`.
    """
    extracted_type = extracted_entities_dict.get("type")
    if extracted_type == "supplier":
        ksc_name = extracted_entities_dict.get("supplier")
        verified_ksc_name = get_highest_similarity_ksc_name(ksc_name, supplier_list)
        if not verified_ksc_name:
            # This handles case where no category has a high enough similarity score
            raise NewsQnAException(
                "Sorry we dont have news for this supplier, please try for a different supplier",
            )

    elif extracted_type == "category":
        if extracted_entities_dict.get("category").lower() != "none":
            ksc_name = extracted_entities_dict.get("category")
            verified_ksc_name = get_highest_similarity_ksc_name(ksc_name, category_list)
            if not verified_ksc_name:
                # Handle case where no category has a high enough similarity score
                raise NewsQnAException(
                    "Sorry we dont have news for this category, "
                    "please try for a different category.",
                )
        else:
            verified_ksc_name = dropdown_selected_category  # USER WROTE "MY CATEGORY"
    elif extracted_type == "keyword":
        raise NewsQnAException(
            "Sorry, we are still working on keyword news implementation",
        )
    else:
        log.error("extracted_type is incorrect")
        raise NewsQnAException(
            "Sorry, we are still working on keyword news implementation",
        )

    log.info("verified_ksc_name is  : %s", verified_ksc_name)
    return verified_ksc_name, extracted_type


def get_highest_similarity_ksc_name(ksc_name: str, ksc_list: list[str], threshold=50):
    """Finds the category in a list with the highest similarity score to ksc_name.

    Args:
        ksc_name: The name retrieved from the extracted entities.
        ksc_list: A list of category names, supplier names or keyword names.
        threshold: Minimum similarity score for a match (default 75).

    Returns:
        The element in ksc_list with the highest similarity score above the
        threshold,
        or "None of the categories match" if no element meets the threshold.
    """

    similarity_scores = [
        (fuzz.ratio(ksc_name.lower(), element.lower()), element) for element in ksc_list
    ]
    score, best_match = max(similarity_scores, key=lambda x: x[0]) if similarity_scores else (0, 0)

    if score >= threshold:
        log.info("best similarity : %s", best_match)
        return best_match

    return None


def get_news_answer(
    news_data: pd.DataFrame,
    user_query: str,
    date_flag: bool,
    mode: str,
    query_type: str,
) -> tuple[str, list[Document]]:
    """Retrieve news-related answer based on user query and news data retrieval.

    Args:
        news_data (pd.DataFrame): DataFrame containing news data.
        user_query (str): User's query.
        date_flag (bool): date_flag
        mode (str): mode
        query_type (str): query_type

    Returns:
        tuple[str, list[Document]]: Response containing relevant information based on the user query
                            along with supporting documents
    """
    vector_store = VectorStoreFactory().faiss_from_news_embeddings(news_data)

    # Todo: handle scenario where query type is not generic / specific
    # if query_type == "generic" or Others:
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "score_threshold": news_conf["generic_threshold"],
            "k": news_conf["generic_top_k"],
        },
    )
    if query_type == "specific":
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "score_threshold": news_conf["specific_threshold"],
                "k": news_conf["specific_top_k"],
            },
        )

    if mode == "synthesis":
        answer, source_documents = generate_qa_chain_response_with_sources(
            user_query=user_query,
            retriever=retriever,
            prompt=news_qna_prompt(date_flag, query_type),
            model=news_conf["model"]["model_name"],
        )
    elif mode == "listing":
        answer, source_documents = generate_qa_chain_response_with_sources(
            user_query=user_query,
            retriever=retriever,
            prompt=news_qna_prompt_list(date_flag),
            model=news_conf["model"]["model_name"],
        )
    else:
        # Todo: need more implementation
        answer, source_documents = ("", [])
        log.error("extracted_mode is neither listing nor synthesis")

    log.info("date flag is %s, mode is %s, query_type is %s", date_flag, mode, query_type)
    return answer, source_documents


def get_news_data(tenant_id: str, date_range: list, ksc_type, ksc_name: str) -> pd.DataFrame:
    """Retrieve news data based on category and date range.

    Args:
        tenant_id (str): received tenant_id in payload
        date_range (list): List containing start_date and end_date.
        ksc_type:
        ksc_name (str): Category of news data to retrieve.

    Returns:
        pd.DataFrame: DataFrame containing news data filtered by category and date range.
    """
    if (
        (date_range is not None)
        and date_range != "NA"
        and date_range[0] != "NA"
        and date_range[1] != "NA"
    ):
        return get_news_data_for_specific_category_and_date(
            tenant_id,
            ksc_type,
            ksc_name,
            date_range,
        )
    return get_news_data_for_specific_category_and_date(tenant_id, ksc_type, ksc_name)


def get_csk_map(pg_db_conn: PGConnector) -> dict[str, list]:
    """Retrieve source to keyword/supplier/category mapping from the news data.

    Args:
        pg_db_conn (PGConnector): PostgreSQL database connector object.
    Returns:
        dict[str, list]: Dictionary containing source as keys and list of corresponding
        keyword/supplier/category as values.
    """
    source_ksc_map = pg_db_conn.select_records_with_filter(
        "news_store",
        filtered_columns=["ksc_name", "source"],
        distinct=True,
    )
    log.info("ksc mapping for tenant: %s", source_ksc_map)
    result_dict: dict[str, list[str]] = {}
    for kcs_name, source in source_ksc_map:
        # Convert source to lowercase
        source_lower = source.lower()
        # If source not in result_dict, add it with an empty list
        if source_lower not in result_dict:
            result_dict[source_lower] = []
        # Append kcs_name to the corresponding source in result_dict
        result_dict[source_lower].append(kcs_name)
    return result_dict
