"""
This file contains the utility functions used for intent classification
"""

import json
import re
from typing import Any

import psycopg2

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import run_conversation_chat
from ada.use_cases.intent_classification.exception import IntentModelUserException
from ada.use_cases.intent_classification.prompts import (
    intent_model_prompt,
    question_enricher_prompt,
)
from ada.utils.config.config_loader import read_config
from ada.utils.format.format import extract_text_in_quotes
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

intent_model_conf = read_config("use-cases.yml")["intent_model_v2"]
log = get_logger("intent_utils")


@log_time
def get_enriched_question(user_query: str, chat_history: list[Any], chat_id: str = "") -> str:
    """
    Based on chat history get the enriched user question which can be answered
    by the models on the next hop
    Args:
        user_query (str): User query from previous hop
        chat_memory (ChatMessageHistory): Chat history object for previous conversations
    Returns:
        (str): Enriched query based on the chat history
    """
    if not chat_history:
        return user_query
    prompt = question_enricher_prompt()
    response = run_conversation_chat(
        chat_history=chat_history,
        prompt=prompt,
        input_str=user_query,
        model=intent_model_conf["model"]["enricher_model_name"],
        window_size=intent_model_conf["model"]["conversation_buffer_window"],
        session_id=chat_id,
    )
    return extract_text_in_quotes(response)


def get_prerequisites_for_individual_request_payloads(json_file: dict) -> dict:
    """
    Get the pre-requisites for the individual request payloads
    Args:
        json_file (dict): Input unified payload
    Returns:
        (dict): Prerequisites for the input requests
    """
    payload_required = {
        "contract-qa": {
            "tenant_id": "",
            "document_id": "",
            "question": [json_file.get("user_query")],
        },
        "source-ai-knowledge": {
            "tenant_id": "",
            "user_input": json_file.get("user_query"),
            "category": "",
            "intent": "source ai knowledge",
        },
        "dynamic-ideas": {
            "tenant_id": "",
            "category": "",
            "request_type": "user_input",
            "user_query": "",
            "intent": "dynamic-ideas",
            "page_id": "",
            "chat_id": "",
        },
        "key-facts-v2": {
            "tenant_id": "",
            "user_id": "dummy",
            "user_query": "",
            "category": "",
            "dax_response_code": None,
            "dax_response": "",
        },
        "news-qna": {"tenant_id": "", "user_query": "", "category": ""},
        "idea-generation-v3": {
            "tenant_id": "",
            "chat_id": "",
            "user_input": json_file.get("user_query"),
            "request_type": "user_input",
            "pinned_elements": {},
        },
        "negotiation-factory": {
            "tenant_id": "",
            "category": "",
            "negotiation_id": json_file.get("chat_id"),
            "request_type": "",
            "user_query": "",
            "pinned_elements": {},
            "selected_elements": {},
        },
    }
    return payload_required


@log_time
def get_intent(
    user_query: str,
    category_name: str,
    chat_history: list[Any],
    chat_id: str = "",
) -> str:
    """
    Get the intent of the user query based on the chat history
    Args:
        user_query (dict): The user query from the ada chat
        category_name (str): Name of the category
        chat_memory (ChatMessageHistory): Chat history object for previous conversations
    Returns:
        (str): Intent str based on the user query and chat history
    """
    intent_value = get_probable_intent(user_query, chat_history)
    if not intent_value or intent_value not in intent_model_conf["intent_model_scope"]:
        prompt = intent_model_prompt(intent_model_conf["intent_model_scope"], category_name)
        intent_value = run_conversation_chat(
            chat_history=chat_history,
            prompt=prompt,
            input_str=user_query,
            model=intent_model_conf["model"]["intent_model_name"],
            window_size=intent_model_conf["model"]["conversation_buffer_window"],
            session_id=chat_id,
        )
    return intent_value.replace('"', "")


@log_time
def get_probable_intent(user_query: str, chat_history: list[Any]) -> str:
    """
    Get the probable intent of the user query based on the chat history
    Args:
        user_query (str): The user query from the ada chat
        chat_memory (list[Any]): Chat history object for previous conversations
    Returns:
        (str): Intent str based on the user query and chat history
    """
    pattern = r"##(.*?)##"
    chat_text = "".join(
        [
            dict(chat).get("request", {}).get("user_query", "")
            for chat in chat_history
            if dict(chat).get("request", {}).get("user_query", "")
        ],
    )
    matched_intent = re.findall(pattern, chat_text)[-1] if re.findall(pattern, chat_text) else ""
    user_query_intent = (
        re.findall(pattern, user_query)[-1] if re.findall(pattern, user_query) else ""
    )
    user_query_intent = user_query_intent.strip()
    if user_query_intent.lower() == "cancel":
        user_query_intent = ""
        matched_intent = ""
        log.info("In cancel workflow")
    else:
        user_query_intent = (
            user_query_intent
            if user_query_intent in intent_model_conf["intent_model_scope"]
            else ""
        )
    log.info("User query intent: %s", user_query_intent)
    log.info("Matched intent: %s", matched_intent)

    intent_value = user_query_intent or matched_intent or ""
    return intent_value


@log_time
def get_chat_history_from_db(chat_id: str, pg_db_conn: PGConnector) -> tuple[Any] | dict[str, Any]:
    """
    Reads the common chat history table and return the list of Realdicts with
    the chat history
    Args:
        chat_id (str): The String of chat id
        pg_db_conn (PGConnector): Postgress connection object
    Returns:
        (tuple): list of Realdicts with the chat history
    """
    chat_history_from_db = pg_db_conn.select_records_with_filter(
        table_name=intent_model_conf["tables"]["chat_history_table"],
        filter_condition=f"chat_id = '{chat_id}' ORDER BY created_time",
    )

    return chat_history_from_db


@log_time
def save_conversation_history(
    chat_id: str,
    request_id: str,
    save_response: dict,
    pg_db_conn: PGConnector,
):
    """
    Saves the conversation history in the chat history table
    Args:
        chat_id (str): Chat id of the session
        request_id (str): Request id of the request
        save_response (dict): Current request, model and response to add to retrieved conversation
        pg_db_conn (PGConnector): PG connector object for writing into database
    """
    try:
        pg_db_conn.insert_values_into_columns(
            intent_model_conf["columns"]["chat_history_table"],
            [
                chat_id,
                request_id,
                save_response["request_type"],
                save_response["request"],
                save_response["model_used"],
                save_response["response_type"],
                save_response["response"],
            ],
            intent_model_conf["tables"]["chat_history_table"],
        )
    except psycopg2.IntegrityError as unique_violation_exception:
        raise IntentModelUserException(
            f"Request ID {request_id} not unique for chat ID {chat_id}",
        ) from unique_violation_exception


def get_response_to_save(
    individual_response: dict,
    individual_request: dict,
    intent_type: str,
) -> dict:
    """
    This functions takes the individual response as a dictionary and intent to
    give the saved response back
    Args:
        individual_response (dict): Individual response dictionary
        individual_request (dict): Individual request dictionary
        intent_type (str): intent_type
    Returns:
        (dict) The request and response to save
    """
    individual_response.pop("additional_data", None)
    individual_response.pop("suppliers_profiles", None)
    individual_request.pop("additional_data", None)
    individual_request.pop("supplier_profiles", None)
    response = (
        individual_response.get("answer", "")
        or individual_response.get("result", [])
        or individual_response.get("message", "")
        or individual_response.get("response", {})
        or individual_response.get("response_prerequisite", "")
    )

    final_response = {
        "response": response,
        "additional_text": individual_response.get("additional_text", ""),
        "links": individual_response.get("links", []),
    }

    optional_params = [
        "arguments",
        "counter_arguments",
        "rebuttals",
        "emails",
        "negotiation_strategy",
        "insights",
        "additional_data",
        "suppliers_profiles",
        "negotiation_approach",
        "suggested_prompts",
        "dynamic_ideas",
    ]

    final_response.update(
        {
            param: individual_response.get(param)
            for param in optional_params
            if individual_response.get(param)
        },
    )

    request = {
        "user_query": individual_request.get("user_query", ""),
    }

    saved_response = {
        "request_type": individual_request.get("request_type", ""),
        "request": json.dumps(request),
        "model_used": intent_type,
        "response_type": individual_response.get("response_type", ""),
        "response": json.dumps(final_response),
    }
    return saved_response


def check_key(required_key: str, source_dict: dict[str, Any]):
    """
    The function checks whether a specific key is present in a dictionary
    and returns the corresponding value if needed.
    Args:
        required_key (str): The key to be checked in the dictionary.
        source_dict (dict[str, Any]): The dictionary where the key is to be checked.
    Raises:
        IntentModelUserException: Raised when the key is missing and user can be informed.
    """
    if required_key not in source_dict:
        error_msg = (
            f"{required_key} is Not available. Please set {required_key} prior to continuing"
        )
        log.error(error_msg)
        raise IntentModelUserException(error_msg)


def add_nf_specific_suggested_prompts(
    unified_response_payload: dict[str, Any],
) -> dict[str, Any]:
    """
    If we receive query from negotiation suggested prompt ,
    add negotiation factory specific suggested prompts if required condition satisfied
    Args:
        unified_response_payload (dict[str, Any]): response payload with all required fields
    Returns:
        (dict[str, Any]): updated response payload with suggested prompts
    """
    unified_response_payload["suggested_prompts"] = unified_response_payload.get(
        "suggested_prompts",
        [],
    )
    return unified_response_payload
