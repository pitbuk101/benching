# import json
import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from ada.use_cases.negotiation_factory.negotiation_factory_utils import PGConnector
from ada.use_cases.negotiation_factory.negotiation_models import (
    generate_arguments,
    generate_arguments_counter_argument_rebuttal_workflow,
    generate_counter_argument_rebuttal,
    generate_user_answers,
)
from ada.utils.config.config_loader import read_config

negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@pytest.fixture
def negotiation_metadata_mock_qa():
    tenant_id = "dummy_tenant_id"
    reference_data = {tenant_id: {}}
    category = "dummy_category"
    negotiation_id = "negotiation_id"
    return tenant_id, reference_data, category, negotiation_id


@pytest.fixture
def negotiation_metadata_mock():
    reference_data = {
        "negotiation_references": pd.DataFrame(
            {
                "l1_objective": "spend",
                "l1_objective_description": "test description",
                "samples": [],
            },
        ),
    }
    category = "test_category"
    return reference_data, category


@pytest.fixture
def supplier_data_mock():
    supplier_name = "test_supplier"
    supplier_relationship = "test relationship"
    supplier_profile = {
        "supplier_name": supplier_name,
        "number_of_sku": 6,
        "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5"],
        "spend_ytd": 1321.99,
        "spend_last_year": 1000.0,
        "currency_symbol": "$",
        "currency_position": "prefix",
        "percentage_spend_across_category_ytd": 12.98,
        "supplier_relationship": supplier_relationship,
    }
    return supplier_name, supplier_profile


@pytest.fixture
def pg_connector_mock():
    with patch(
        "ada.use_cases.negotiation_factory.negotiation_factory_utils.PGConnector",
        spec=PGConnector,
    ) as mock_obj:
        yield mock_obj.return_value


@patch("ada.use_cases.negotiation_factory.negotiation_models.generate_chat_response")
@patch(
    "ada.use_cases.negotiation_factory.negotiation_models.generate_conversational_rag_agent_response",
)
@patch("ada.use_cases.negotiation_factory.negotiation_models.argument_prompt")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.fetch_insights_for_supplier")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_model_context")
@patch("ada.use_cases.negotiation_factory.negotiation_models.update_negotiation_details")
def test_generate_arguments_without_previous_arguments(
    update_negotiation_details_mock,
    extract_model_context_mock,
    fetch_insights_for_supplier_mock,
    argument_prompt_mock,
    generate_chat_response_mock,
    generate_conversational_rag_agent_response_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    supplier_data_mock,
):
    reference_data, category = negotiation_metadata_mock
    (
        supplier_name,
        supplier_profile,
    ) = supplier_data_mock
    user_query = "generate Arguments for spend"
    chat_history = []

    negotiation_objective_description = [
        "test objective description 1",
        "test objective description 2",
    ]
    pinned_objectives = [
        {
            "id": "I3",
            "objective": "label_3",
            "objective_type": "objective_1",
            "objective_reinforcements": ["reinforcements_4", "reinforcements_5"],
            "list_of_skus": [],
            "target": "515000",
            "current_value": "538000",
        },
        {
            "id": "I4",
            "objective": "label_4",
            "objective_type": "objective_1",
            "objective_reinforcements": ["reinforcements_4", "reinforcements_1"],
            "list_of_skus": [],
            "target": "515000",
            "current_value": "538000",
        },
    ]
    pinned_elements = {"objectives": pinned_objectives, "supplier_profile": supplier_profile}
    selected_elements = {"counter_arguments": [], "rebuttals": []}

    extract_model_context_mock.return_value = (
        supplier_name,
        supplier_profile,
        negotiation_objective_description,
    )

    formatted_arguments_details = [
        {"id": "arguments_1", "details": "test argument 1"},
        {"id": "arguments_2", "details": "test argument 2"},
    ]
    response = {
        "message": f"Arguments generated for supplier {supplier_name} using the pinned objective: ",
        "arguments": formatted_arguments_details,
    }

    generate_chat_response_mock.return_value = {"generation": json.dumps(response)}
    generate_conversational_rag_agent_response_mock.return_value = {
        "generation": json.dumps(response),
    }

    expected_data = {
        "response_type": "arguments",
        "message": "Arguments generated for supplier test_supplier using the pinned objective: ",
        "suggested_prompts": [
            {
                "prompt": "Generate new arguments",
                "intent": "negotiation_arguments_new",
            },
            {
                "prompt": "Reply to supplier arguments",
                "intent": "negotiation_arguments_reply",
            },
            {
                "prompt": "Generate negotiation email",
                "intent": "negotiation_emails",
            },
        ],
        "arguments": [
            {
                "id": "arguments_1",
                "details": "test argument 1",
            },
            {
                "id": "arguments_2",
                "details": "test argument 2",
            },
        ],
    }

    pg_connector_mock.search_by_vector_similarity.return_value = pd.DataFrame(
        columns=["embedding", "chunk_content", "page"],
        data={
            "embedding": [
                json.dumps([0.1, 0.2, 0.3, 0.4]),
                json.dumps([0.4, 0.2, 0.3, 0.4]),
                json.dumps([0.1, 0.6, 0.3, 0.49]),
                json.dumps([0.1, 0.23, 0.3, 0.4]),
                json.dumps([0.8, 0.2, 0.9, 0.4]),
            ],
            "chunk_content": [
                "test_content1",
                "test_content2",
                "test_content3",
                "test_content4",
                "test_content5",
            ],
            "page": [1, 2, 3, 4, 5],
        },
    )
    update_negotiation_details_mock.return_value = formatted_arguments_details

    actual_data = generate_arguments(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        chat_history,
        selected_elements,
        generation_type="arguments",
    )

    assert expected_data == actual_data


def test_generate_arguments_without_previous_arguments_and_insights(
    pg_connector_mock,
    negotiation_metadata_mock,
):
    reference_data, category = negotiation_metadata_mock
    user_query = "generate Arguments for spend"
    pinned_elements = {}
    selected_elements = {
        "arguments": [],
        "counter_arguments": [],
        "rebuttals": [],
    }

    expected_data = {
        "response_type": "negotiation_arguments",
        "message": (
            "To effectively work with arguments, it's imperative to have objective "
            "pinned/selected.Please select `Set negotiation objectives` to proceed further."
        ),
        "suggested_prompts": [
            {
                "prompt": negotiation_conf["cta_button_map"]["objective"],
                "intent": "negotiation_objective",
            },
            {
                "prompt": negotiation_conf["cta_button_map"]["emails"],
                "intent": "negotiation_emails",
            },
        ],
    }

    actual_data = generate_arguments_counter_argument_rebuttal_workflow(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        [],
        selected_elements,
        generation_type="negotiation_arguments",
    )

    assert expected_data == actual_data


@patch("ada.use_cases.negotiation_factory.negotiation_models.update_negotiation_details")
@patch("ada.use_cases.negotiation_factory.negotiation_models.run_conversation_chat")
@patch(
    "ada.use_cases.negotiation_factory.negotiation_models.generate_conversational_rag_agent_response",
)
@patch("ada.use_cases.negotiation_factory.negotiation_models.counter_argument_rebuttal_prompt")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.fetch_insights_for_supplier")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_model_context")
def test_generate_counter_arguments(
    extract_model_context_mock,
    fetch_insights_for_supplier_mock,
    counter_argument_rebuttal_prompt_mock,
    generate_chat_response_mock,
    generate_conversational_rag_agent_response_mock,
    update_negotiation_details_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    supplier_data_mock,
):
    reference_data, category = negotiation_metadata_mock
    (
        supplier_name,
        supplier_profile,
    ) = supplier_data_mock

    negotiation_objective_description = ["test objective description"]

    extract_model_context_mock.return_value = (
        supplier_name,
        supplier_profile,
        negotiation_objective_description,
    )

    user_query = negotiation_conf["cta_button_map"]["counter_arguments"]
    chat_history = []

    arguments = [
        {"id": "arguments_1", "details": "test argument 1"},
    ]

    pinned_elements = {
        "supplier_profile": supplier_profile,
        "arguments": arguments,
        "objectives": [
            {
                "id": "1",
                "objective": "test_insight",
                "objective_type": "Price reduction",
                "objective_reinforcements": "",
                "list_of_skus": [],
                "target": "555000",
                "current_value": "538000",
                "objective_param": "PRICE",
                "unit": "NUMBER",
            },
        ],
    }
    selected_elements = {}

    supplier_carrot_insights = [
        {
            "id": "I11",
            "insight": "label_11",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["carrot", "unknown"],
            "list_of_skus": [],
        },
        {
            "id": "I12",
            "insight": "label_12",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["stick", "carrot"],
            "list_of_skus": [],
        },
    ]

    fetch_insights_for_supplier_mock.return_value = supplier_carrot_insights

    prompt = MagicMock()
    counter_argument_rebuttal_prompt_mock.return_value = prompt

    response = "test_header_1|test counter argument 1"
    generate_chat_response_mock.return_value = {"generation": response}
    generate_conversational_rag_agent_response_mock.return_value = {"generation": response}

    formatted_counter_arguments_details = [
        {
            "id": "counter_arguments_1",
            "raw": "test counter argument 1",
            "details": "test counter argument 1",
        },
    ]
    update_negotiation_details_mock.return_value = formatted_counter_arguments_details
    expected_data = {
        "response_type": "counter_arguments",
        "message": ("Counter arguments generated for supplier test_supplier "),
        "suggested_prompts": [
            {
                "prompt": "Modify counter arguments",
                "intent": "negotiation_counter_arguments_modify",
            },
            {
                "prompt": "Generate new arguments",
                "intent": "negotiation_arguments_new",
            },
            {
                "prompt": negotiation_conf["cta_argument_map"]["arguments_reply"],
                "intent": "negotiation_arguments_reply",
            },
            {
                "prompt": negotiation_conf["cta_button_map"]["emails"],
                "intent": "negotiation_emails",
            },
        ],
        "counter_arguments": [
            {
                "id": "counter_arguments_1",
                "raw": "test counter argument 1",
                "reference_id": "arguments_1",
                "reference_raw": "test argument 1",
                "details": (
                    "** Arguments ** \ntest argument 1\n"
                    " **Ada's reply ** \ntest counter argument 1"
                ),
            },
        ],
    }
    pg_connector_mock.search_by_vector_similarity.return_value = pd.DataFrame(
        columns=["embedding", "chunk_content", "page"],
        data={
            "embedding": [
                json.dumps([0.1, 0.2, 0.3, 0.4]),
                json.dumps([0.4, 0.2, 0.3, 0.4]),
                json.dumps([0.1, 0.6, 0.3, 0.49]),
                json.dumps([0.1, 0.23, 0.3, 0.4]),
                json.dumps([0.8, 0.2, 0.9, 0.4]),
            ],
            "chunk_content": [
                "test_content1",
                "test_content2",
                "test_content3",
                "test_content4",
                "test_content5",
            ],
            "page": [1, 2, 3, 4, 5],
        },
    )
    actual_data = generate_counter_argument_rebuttal(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        chat_history,
        selected_elements,
        generation_type="negotiation_counter_arguments",
    )

    assert expected_data == actual_data

    update_negotiation_details_mock.assert_called_once_with(
        generated_details=response.split("|"),
        previous_ids=[],
    )


def test_generate_counter_arguments_when_not_call_directly_with_counter_arguments(
    pg_connector_mock,
    negotiation_metadata_mock,
):
    reference_data, category = negotiation_metadata_mock
    user_query = "Generate counter arguments"
    chat_history = []
    pinned_elements = {
        "supplier_profile": MagicMock(),
    }
    selected_elements = {
        "arguments": [],
        "counter_arguments": [],
        "rebuttals": [],
    }

    expected_data = {
        "response_type": "negotiation_counter_arguments",
        "message": (
            "To effectively work with arguments, it's imperative to have objective pinned/selected."
            "Please select `Set negotiation objectives` to proceed further."
        ),
        "suggested_prompts": [
            {
                "prompt": negotiation_conf["cta_button_map"]["objective"],
                "intent": "negotiation_objective",
            },
            {
                "prompt": negotiation_conf["cta_button_map"]["emails"],
                "intent": "negotiation_emails",
            },
        ],
    }
    actual_data = generate_arguments_counter_argument_rebuttal_workflow(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        chat_history,
        selected_elements,
        generation_type="negotiation_counter_arguments",
        call_directly=False,
    )
    assert expected_data == actual_data


@patch("ada.use_cases.negotiation_factory.negotiation_models.run_conversation_chat")
@patch("ada.use_cases.negotiation_factory.negotiation_models.user_query_prompt")
@patch("ada.use_cases.negotiation_factory.negotiation_models.extract_qa_context")
@patch("ada.use_cases.negotiation_factory.negotiation_models.extract_objective_description")
def test_generate_user_answers(
    extract_objective_description_mock,
    extract_qa_context_mock,
    user_query_prompt_mock,
    run_conversation_chat_mock,
    pg_connector_mock,
    negotiation_metadata_mock_qa,
):
    tenant_id, reference_data, category, _ = negotiation_metadata_mock_qa
    user_query = "How negotiation will help me"

    supplier_name = "test_supplier_name"
    supplier_relationship = "test relationship"

    supplier_profile = {
        "supplier_name": supplier_name,
        "number_of_sku": 6,
        "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5"],
        "spend_ytd": 1321.99,
        "spend_last_year": 1000.0,
        "currency_symbol": "$",
        "currency_position": "prefix",
        "percentage_spend_across_category_ytd": 12.98,
        "supplier_relationship": supplier_relationship,
    }
    pinned_elements = {"supplier_profile": supplier_profile}

    objective_description = "test objective description"
    extract_objective_description_mock.return_value = objective_description

    category_qna, supplier_qna, sku_qna = "test category qna", "test supplier qna", "test sku qna"
    extract_qa_context_mock.return_value = (
        category_qna,
        supplier_qna,
        sku_qna,
    )

    user_query_prompt_mock.return_value = "test prompt"

    response = "test response of user question"
    run_conversation_chat_mock.return_value = response

    expected_data = {
        "response_type": "user_questions",
        "message": response,
        "suggested_prompts": [
            {
                "intent": "negotiation_approach_cp",
                "prompt": negotiation_conf["cta_button_map"]["approach_cp"],
            },
            {
                "intent": "negotiation_objective",
                "prompt": negotiation_conf["cta_button_map"]["objective"],
            },
            {
                "intent": "negotiation_insights",
                "prompt": negotiation_conf["cta_button_map"]["insights"],
            },
        ],
    }
    actual_data = generate_user_answers(
        reference_data.get(tenant_id),
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        [],
    )

    assert expected_data == actual_data
    extract_qa_context_mock.assert_called_once_with(
        pg_connector_mock,
        category,
        supplier_name,
        supplier_profile.get("sku_list"),
    )
    user_query_prompt_mock.assert_called_once_with(
        category,
        category_qna,
        supplier_profile,
        supplier_qna,
        sku_qna,
        "",
        negotiation_conf["negotiation_factory_description"],
        pinned_elements,
    )


@patch("ada.use_cases.negotiation_factory.negotiation_models.run_conversation_chat")
@patch("ada.use_cases.negotiation_factory.negotiation_models.user_query_prompt")
@patch("ada.use_cases.negotiation_factory.negotiation_models.extract_qa_context")
@patch("ada.use_cases.negotiation_factory.negotiation_models.extract_objective_description")
def test_generate_user_answers_no_supplier_profile(
    extract_objective_description_mock,
    extract_qa_context_mock,
    user_query_prompt_mock,
    run_conversation_chat_mock,
    pg_connector_mock,
    negotiation_metadata_mock_qa,
):
    tenant_id, reference_data, category, _ = negotiation_metadata_mock_qa
    user_query = "How negotiation will help me"
    pinned_elements = {}
    objective_description = "test objective description"
    extract_objective_description_mock.return_value = objective_description

    category_qna, supplier_qna, sku_qna = "test category qna", "test supplier qna", "test sku qna"
    extract_qa_context_mock.return_value = (
        category_qna,
        supplier_qna,
        sku_qna,
    )

    user_query_prompt_mock.return_value = "test prompt"

    response = "test response of user question"
    run_conversation_chat_mock.return_value = response

    expected_data = {
        "response_type": "user_questions",
        "message": response,
        "suggested_prompts": [],
    }
    actual_data = generate_user_answers(
        reference_data.get(tenant_id),
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        [],
        selected_elements=None,
    )
    assert expected_data == actual_data
    extract_qa_context_mock.assert_called_once_with(
        pg_connector_mock,
        category,
        None,
        [],
    )
    user_query_prompt_mock.assert_called_once_with(
        category,
        category_qna,
        {},
        supplier_qna,
        sku_qna,
        "",
        negotiation_conf["negotiation_factory_description"],
        {},
    )
