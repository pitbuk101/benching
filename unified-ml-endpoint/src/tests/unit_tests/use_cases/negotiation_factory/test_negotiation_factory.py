from __future__ import annotations

import json
import warnings
from unittest.mock import ANY, patch

import pytest

from ada.use_cases.negotiation_factory.negotiation_factory import (
    get_intent,
    run_negotiation_factory,
)
from ada.utils.config.config_loader import read_config

warnings.filterwarnings("ignore", category=DeprecationWarning)

negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@pytest.fixture
def negotiation_metadata_mock():
    tenant_id = "dummy_tenant_id"
    reference_data = {tenant_id: {}}
    category = "dummy_category"
    negotiation_id = "negotiation_id"
    return tenant_id, reference_data, category, negotiation_id


@pytest.fixture
def pg_connector_mock():
    with patch("ada.use_cases.negotiation_factory.negotiation_factory.PGConnector") as mock_obj:
        yield mock_obj.return_value


@patch("ada.use_cases.negotiation_factory.negotiation_factory.run_conversation_chat")
def test_get_intent(run_conversation_chat_mock, negotiation_metadata_mock):
    _, _, category, _ = negotiation_metadata_mock
    user_query = "Show insights"
    chat_history = []
    ai_response = "test ai response"
    run_conversation_chat_mock.return_value = ai_response

    expected_data = (f"""negotiation_{ai_response}""", user_query)

    actual_data = get_intent(chat_history, category, user_query, selected_elements={})
    assert expected_data == actual_data
    run_conversation_chat_mock.assert_called_once_with(
        chat_history=chat_history,
        prompt=ANY,
        input_str=user_query,
        memory_type="window",
        model=negotiation_conf["model"]["model_name"],
        window_size=negotiation_conf["model"]["conversation_buffer_window"],
        temperature=0,
        input_message_key="input",
        history_message_key="history",
        session_id="",
    )


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory.generate_arguments_counter_argument_rebuttal_workflow",
)
@patch("ada.use_cases.negotiation_factory.negotiation_factory.get_intent")
def test_run_negotiation_factory(
    get_intent_mock,
    generate_arguments_counter_arguments_rebuttals_mock,
    negotiation_metadata_mock,
    pg_connector_mock,
):
    tenant_id, reference_data, category, negotiation_id = negotiation_metadata_mock
    user_query = "Generate Arguments"
    chat_history = []
    pinned_elements = {}
    selected_elements = {}
    request_type = ""
    input_data = {
        "tenant_id": tenant_id,
        "category": category,
        "negotiation_id": negotiation_id,
        "user_query": user_query,
        "pinned_elements": pinned_elements,
        "request_type": request_type,
        "before_update_request_type": "",
    }

    identified_request_type = "negotiation_arguments_generics"
    get_intent_mock.return_value = (identified_request_type, user_query)

    expected_response = {
        "response_type": "arguments",
        "message": "test msg",
        "suggested_prompts": [],
    }
    generate_arguments_counter_arguments_rebuttals_mock.return_value = expected_response

    actual_response = run_negotiation_factory(
        json.dumps(input_data),
        reference_data,
        pg_connector_mock,
        chat_history,
    )

    assert expected_response == actual_response
    get_intent_mock.assert_called_once_with(
        chat_history=chat_history,
        category=category,
        user_query=user_query,
        selected_elements={},
    )

    generate_arguments_counter_arguments_rebuttals_mock.assert_called_once_with(
        pg_db_conn=pg_connector_mock,
        category=category,
        user_query=user_query,
        pinned_elements=pinned_elements,
        chat_history=chat_history,
        reference_data=reference_data.get(tenant_id),
        selected_elements=selected_elements,
        generation_type="negotiation_arguments_generics",
        chat_id="negotiation_id",
        before_update_request_type="",
        current_round=1,
    )


def test_run_negotiation_factory_without_all_required_fields(negotiation_metadata_mock):
    tenant_id, reference_data, category, negotiation_id = negotiation_metadata_mock
    user_query = "Generate Arguments"

    input_data = {
        "tenant_id": tenant_id,
        "category": category,
        "negotiation_id": negotiation_id,
        "user_query": user_query,
    }

    expected_response = {
        "response_type": "exception",
        "message": "pinned_elements is missing in the Payload",
        "suggested_prompts": [],
    }

    actual_response = run_negotiation_factory(
        json.dumps(input_data),
        reference_data.get(tenant_id),
        pg_connector_mock,
        [],
    )
    assert actual_response == expected_response


def test_run_negotiation_factory_with_invalid_negotiation_id(negotiation_metadata_mock):
    tenant_id, reference_data, category, negotiation_id = negotiation_metadata_mock
    invalid_negotiation_id = [negotiation_id]
    user_query = "Generate Arguments"
    pinned_elements = {}
    request_type = ""
    input_data = {
        "tenant_id": tenant_id,
        "category": category,
        "negotiation_id": invalid_negotiation_id,
        "user_query": user_query,
        "pinned_elements": pinned_elements,
        "request_type": request_type,
    }

    expected_response = {
        "response_type": "exception",
        "message": "Negotiation Id is not correct.",
        "suggested_prompts": [],
    }

    actual_response = run_negotiation_factory(
        json.dumps(input_data),
        reference_data.get(tenant_id),
        pg_connector_mock,
        [],
    )

    assert actual_response == expected_response
