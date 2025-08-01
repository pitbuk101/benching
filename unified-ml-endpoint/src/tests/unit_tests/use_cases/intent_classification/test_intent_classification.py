import ast
import os
import pathlib
import random
import uuid
from unittest.mock import patch

import pandas as pd
import pytest

from ada.use_cases.intent_classification.intent_classification_v2 import (
    get_individual_request_payload,
    get_unified_response,
    model_router,
)
from ada.use_cases.intent_classification.intent_utils import (  # get_enriched_question,
    add_nf_specific_suggested_prompts,
    get_chat_history_from_db,
    get_intent,
    get_response_to_save,
)
from ada.utils.config.config_loader import read_config
from ada.utils.metrics.context_manager import UseCase

intent_model_scope = read_config("use-cases.yml")["intent_model_v2"]["intent_model_scope"][0]
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]
data_dir = os.path.join(pathlib.Path(__file__).parents[4], "data")


def mock_contract_qa_function(*args, **kwargs) -> dict:
    """
    Mock run function for contract_qa
    """
    mock_mapping = get_individual_response()
    return mock_mapping["contract-qa"]["output"]


def mock_source_ai_knowledge_function(*args) -> dict:
    """
    Mock run function for idea generation
    """
    mock_mapping = get_individual_response()
    return mock_mapping["source-ai-knowledge"]["output"]


def mock_idea_generation_v2_dev_function(*args) -> dict:
    """
    Mock run function for idea generation v2 dev
    """
    mock_mapping = get_individual_response()
    return mock_mapping["idea-generation-v3"]["output"]


def mock_key_facts_function(*args, **kwargs) -> dict:
    """
    Mock run function for key facts
    """
    mock_mapping = get_individual_response()
    return mock_mapping["key-facts-v2"]["output"]


def mock_negotiation_factory_function(*args, pg_db_conn) -> dict:
    """
    Mock run function for negotiation factory
    """
    mock_mapping = get_individual_response()
    return mock_mapping["negotiation-factory"]["output"]


def get_individual_response() -> dict:
    return {
        "contract-qa": {
            "use_case": UseCase.CONTRACT_QANDA,
            "run": mock_contract_qa_function,
            "output": [
                {
                    "question": "what is the payment terms for this contract?",
                    "answer": "The payment terms of this contract is 13 days against a 21 day benchmark",
                    "sources": "",
                },
            ],
        },
        "source-ai-knowledge": {
            "use_case": UseCase.KNOWLEDGE_DOC,
            "run": mock_source_ai_knowledge_function,
            "output": {
                "result": "response from doc QnA",
                "response_type": "source-ai-knowledge",
            },
        },
        "key-facts-v2": {
            "use_case": UseCase.KEY_FACTS,
            "run": mock_key_facts_function,
            "output": {
                "response_type": "dax",
                "response_prerequisite": "dax_query_custom_filtered",
                "owner": "ai",
                "additional_text": "additional_text",
                "message": "the keyfacts value is 34",
                "links": ["link1", "link2"],
            },
        },
        "idea-generation-v3": {
            "use_case": UseCase.IDEA_GEN,
            "run": mock_idea_generation_v2_dev_function,
            "output": {
                "chat_id": "122abc",
                "response_type": "rca",
                "response": {
                    "root_causes": ["root_cause1", "root_cause2", "root_cause3"],
                    "ideas": [],
                    "answer": "",
                    "linked_insights": [],
                },
            },
        },
        "negotiation-factory": {
            "use_case": UseCase.NEGO_FACTORY,
            "run": mock_negotiation_factory_function,
            "output": {
                "response_type": "arguments",
                "message": "",
                "negotiation_oobjective": "",
                "arguments": ["argument1", "argument2", "argument3"],
                "suggested_prompts": [
                    {"prompt": "Generate Counters", "intent": "counter_arguments"},
                ],
            },
        },
    }


def get_uniformed_input_json() -> dict:
    return {
        "contract-qa": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "user_query": "what is the payment terms for this contract?",
        },
        "source-ai-knowledge": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "user_query": "How do we negotiate with supplier based on insights?",
        },
        "key-facts-v2": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "Bearings",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "user_query": "What is spend break down across different sub-categories for last 12 months?",
            "dax_response_code": 403,
            "dax_response": "dummy",
        },
        "idea-generation-v3": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "chat_id": "122abc",
            "request_type": "rca",
            "request_id": "",
            "pinned_elements": {
                "pinned_insights": [
                    {
                        "insight": (
                            "The total cleansheet gap identified in last 12 months "
                            "for bearings category is up to 2.9M EUR."
                        ),
                        "is_main": "1",
                        "insight_id": "2083021635",
                    },
                ],
                "pinned_root_causes": [],
                "pinned_ideas": [],
            },
            "more_info": [],
            "linked_insights": [{}],
            "general_info": {},
            "user_query": "Can you expand on the root causes?",
        },
        "negotiation-factory": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "user_query": "Generate negotiation arguments for SKG FRANCE.",
        },
    }


def get_individual_input_json() -> dict:
    return {
        "contract-qa": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "document_id": "",
            "user_query": "what is the payment terms for this contract?",
            "question": ["what is the payment terms for this contract?"],
        },
        "source-ai-knowledge": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "user_query": "How do we negotiate with supplier based on insights?",
            "user_input": "How do we negotiate with supplier based on insights?",
            "intent": "source ai knowledge",
        },
        "key-facts-v2": {
            "user_id": "dummy",
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "Bearings",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "user_query": "What is spend break down across different sub-categories for last 12 months?",
            "dax_response_code": 403,
            "dax_response": "dummy",
        },
        "idea-generation-v3": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "chat_id": "122abc",
            "user_input": "Can you expand on the root causes?",
            "user_query": "Can you expand on the root causes?",
            "request_type": "rca",
            "request_id": "",
            "pinned_elements": {
                "pinned_insights": [
                    {
                        "insight": (
                            "The total cleansheet gap identified in last 12 months "
                            "for bearings category is up to 2.9M EUR."
                        ),
                        "is_main": "1",
                        "insight_id": "2083021635",
                    },
                ],
                "pinned_root_causes": [],
                "pinned_ideas": [],
            },
            "more_info": [],
            "linked_insights": [{}],
            "general_info": {},
        },
        "negotiation-factory": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "",
            "page_id": "",
            "chat_id": "123",
            "request_id": "",
            "negotiation_id": "123",
            "request_type": "",
            "user_query": "Generate negotiation arguments for SKG FRANCE.",
            "pinned_elements": {},
            "selected_elements": {},
        },
    }


def get_unified_response_keys() -> set:
    return {
        "chat_id",
        "message",
        "request_id",
    }


def get_save_response_keys() -> set:
    return {
        "model_used",
        "request",
        "request_type",
        "response",
        "response_type",
    }


def get_mock_data_for_input_payload() -> list:
    """
    Creates a mock intent, input, output payload for tests
    Returns:
        (dict): Mock payload for each of the use cases in scope
    """
    unified_input_payload = get_uniformed_input_json()
    individual_input_payload = get_individual_input_json()
    return [
        (key, value, individual_input_payload[key]) for key, value in unified_input_payload.items()
    ]


def get_mock_data_for_input_output_payload() -> list:
    """
    Creates a mock intent, input, output payload for tests
    Returns:
        (dict): Mock payload for each of the use cases in scope
    """
    input_payload = get_individual_input_json()
    output_payload = get_individual_response()
    return [(key, value, output_payload[key]["output"]) for key, value in input_payload.items()]


def setup_mock_pg_connector():
    """
    Setup mock environment for PGConnector.
    Returns:
        MagicMock: Mocked instance of PGConnector.
    """
    return_records = """[[('chat_id', '123'), ('request_id', ''), ('model_used', 'news-qna'),
    ('request', {"tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f", "category": "Bearings", "page_id": "", "chat_id": "123", "request_id": "", "user_query": "What is the summary of the latest news in Bearings?"}), ('response', '{"message": " According to the provided news data, RBC Bearings latest market cap is $7.99 billion", "response_type": "summary"], "additional_text": "For more information, please visit below links .. "}')]]"""  # noqa: E501

    with patch("ada.components.db.pg_connector.PGConnector") as MockPGConnector:
        # Create an instance of the mocked PGConnector
        mock_pg_db_conn = MockPGConnector.return_value
        # Mock the return value of select_records_with_filter function
        mock_pg_db_conn.select_records_with_filter.return_value = ast.literal_eval(return_records)
        # Mock the return value of insert_values_into_columns function
        mock_pg_db_conn.insert_values_into_columns.return_value = None
        # Return the mocked instance
        return mock_pg_db_conn


@pytest.mark.parametrize(
    "intent_type, input_json",
    [
        (key, value)
        for key, value in get_uniformed_input_json().items()
        if key in intent_model_scope
    ],
)
def test_model_router(intent_type, input_json):
    mock_pg_db_conn = setup_mock_pg_connector()
    chat_history = get_chat_history_from_db(input_json["chat_id"], mock_pg_db_conn)
    with patch(
        """ada.use_cases.intent_classification.intent_classification_v2.function_mapping""",
        return_value=get_individual_response(),
    ):
        input_json["request_id"] = uuid.uuid4().hex[:6].upper()

        unified_response_payload = model_router(
            intent_type,
            input_json,
            mock_pg_db_conn,
            chat_history,
            category_configuration=pd.DataFrame(),
            question_classifier_model={},
            all_reference_data={"negotiation-factory": {}},
        )
    assert isinstance(unified_response_payload, dict) and set(get_unified_response_keys()).issubset(
        set(unified_response_payload.keys()),
    )


# unified_request_transformer
@pytest.mark.parametrize("intent_type, input_json, output_json", get_mock_data_for_input_payload())
def test_get_individual_request_payload(intent_type, input_json, output_json):
    assert get_individual_request_payload(input_json, intent_type) == output_json


@pytest.mark.parametrize(
    "intent_type, input_query",
    [
        (key, value["user_query"])
        for key, value in get_individual_input_json().items()
        if key in intent_model_scope
    ],
)
def test_intent_model(intent_type, input_query):
    _, input_json = random.choice(list(get_individual_input_json().items())) #NOSONAR
    mock_pg_db_conn = setup_mock_pg_connector()
    chat_history = get_chat_history_from_db(input_json.get("chat_id", ""), mock_pg_db_conn)
    assert (
        get_intent(
            input_query,
            category_name="category",
            chat_history=chat_history,
            chat_id=input_json.get("chat_id", ""),
        )
        == intent_type
    )


@pytest.mark.parametrize("intent_type, input, response", get_mock_data_for_input_output_payload())
def test_get_response_to_save(intent_type, input, response):
    if isinstance(response, list):
        response = response[0]
    save_response = get_response_to_save(response, input, intent_type)
    assert isinstance(save_response, dict) and (
        set(save_response.keys()) == set(get_save_response_keys())
    )
    for value in save_response.values():
        assert isinstance(value, str), f"Value '{value}' is not a string"
    assert save_response["model_used"] == intent_type


# @pytest.mark.parametrize(
#     "question",
#     [
#         value["user_query"]
#         for key, value in get_individual_input_json().items()
#         if key in intent_model_scope
#     ],
# )
# def test_get_enriched_question(question):
#     _, input_json = random.choice(list(get_individual_input_json().items())) #NOSONAR
#     mock_pg_db_conn = setup_mock_pg_connector()
#     chat_history = get_chat_history_from_db(input_json["chat_id"], mock_pg_db_conn)
#     chat_memory = get_chat_message_history(chat_history)
#     print(get_enriched_question(question, chat_memory))


@pytest.mark.parametrize(
    ("input_json, individual_response"),
    [
        (input_json, output_json)
        for intent, input_json, output_json in get_mock_data_for_input_output_payload()
        if intent in intent_model_scope
    ],
)
def test_get_unified_response(input_json, individual_response):
    input_json["request_id"] = uuid.uuid4().hex[:6].upper()
    response = get_unified_response(individual_response, input_json)
    assert isinstance(response, dict) and set(get_unified_response_keys()).issubset(
        set(response.keys()),
    )


def test_add_nf_specific_suggested_prompts():
    response_payload = {
        "message": "test message",
    }

    expected_prompts = []
    expected_data = {
        **response_payload,
        "suggested_prompts": expected_prompts,
    }

    actual_data = add_nf_specific_suggested_prompts(
        response_payload,
    )

    assert expected_data == actual_data
