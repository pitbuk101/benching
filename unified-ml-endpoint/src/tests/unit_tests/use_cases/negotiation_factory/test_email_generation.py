from unittest.mock import MagicMock, patch

import pytest

from ada.use_cases.negotiation_factory.email_generation import (
    append_email_to_thread,
    generate_email,
    generate_email_thread,
)
from ada.utils.config.config_loader import read_config

negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@pytest.fixture
def suggested_prompt():
    return [
        {
            "prompt": negotiation_conf["cta_email_map"]["negotiation_emails_reply_to_supplier"],
            "intent": "negotiation_emails_reply_to_supplier",
        },
        {
            "intent": "negotiation_emails_continue",
            "prompt": negotiation_conf["cta_email_map"]["negotiation_emails_continue"],
        },
        {
            "intent": "negotiation_emails",
            "prompt": negotiation_conf["cta_email_map"]["negotiation_emails"],
        },
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
    ]


@pytest.fixture
def input_data():
    reference_data = {}
    pg_db_conn = MagicMock()
    category = "test_category"
    chat_history = [{"response_type": "emails"}]
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
    selected_elements = {}
    return (
        reference_data,
        pg_db_conn,
        category,
        chat_history,
        supplier_name,
        supplier_profile,
        supplier_relationship,
        selected_elements,
    )


@pytest.fixture
def mock_dependencies():
    with (
        patch(
            "ada.use_cases.negotiation_factory.email_generation.extract_model_context",
        ) as extract_model_context_mock,
        patch(
            "ada.use_cases.negotiation_factory.email_generation.generate_conversational_rag_agent_response",
        ) as run_conversation_chat_mock,
        patch(
            "ada.use_cases.negotiation_factory.email_generation.append_email_to_thread",
        ) as append_email_to_thread_mock,
        patch(
            "ada.use_cases.negotiation_factory.email_generation.email_prompt",
        ) as email_prompts_mock,
        patch(
            "ada.use_cases.negotiation_factory.email_generation.generate_email",
        ) as generate_email_mock,
        patch(
            "ada.use_cases.negotiation_factory.negotiation_factory_utils.fetch_insights_for_supplier",
        ) as fetch_insights_for_supplier_mock,
        patch(
            "ada.use_cases.negotiation_factory.negotiation_factory_utils.get_samples",
        ) as get_samples_mock,
    ):
        yield (
            extract_model_context_mock,
            run_conversation_chat_mock,
            append_email_to_thread_mock,
            email_prompts_mock,
            generate_email_mock,
            fetch_insights_for_supplier_mock,
            get_samples_mock,
        )


@pytest.fixture
def pg_retriever_mock():
    with patch(
        "ada.use_cases.negotiation_factory.email_generation.PGRetriever",
    ) as mock_obj:
        yield mock_obj.return_value


def test_generate_email_without_pinned_insights(mock_dependencies, suggested_prompt, input_data):
    (
        extract_model_context_mock,
        _,
        append_email_to_thread_mock,
        _,
        generate_email_mock,
        _,
        _,
    ) = mock_dependencies
    (
        reference_data,
        pg_db_conn,
        category,
        chat_history,
        supplier_name,
        supplier_profile,
        supplier_relationship,
        selected_elements,
    ) = input_data
    user_query = f"Generate email to negotiate with {supplier_name}. Set up a meeting on the 15th"

    negotiation_objective_description = ["test objective description"]

    pinned_elements = {
        "supplier_profile": supplier_profile,
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

    extract_model_context_mock.return_value = (
        supplier_name,
        supplier_profile,
        negotiation_objective_description,
    )

    generate_email_mock.return_value = {"emails": "dummy_response"}

    append_email_to_thread_mock.return_value = []

    expected_data = {
        "response_type": "emails",
        "message": "Please find the draft email below: ",
        "suggested_prompts": [
            {"prompt": "Modify email", "intent": "negotiation_emails_modify"},
            {"prompt": "Reply to supplier email", "intent": "negotiation_emails_reply_to_supplier"},
            {"prompt": "Generate a follow-up email", "intent": "negotiation_emails_continue"},
        ],
        "supplier_profile": supplier_profile,
        "emails": [],
    }
    actual_data = generate_email_thread(
        reference_data,
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        chat_history,
        selected_elements,
    )

    assert expected_data == actual_data


def test_generate_email_thread_cta(input_data):
    (
        reference_data,
        pg_db_conn,
        category,
        chat_history,
        _,
        _,
        _,
        selected_elements,
    ) = input_data
    generate_email_thread(
        reference_data,
        pg_db_conn,
        category,
        "reply to supplier email",
        {},
        chat_history,
        selected_elements,
        generation_type="negotiation_emails_reply_to_supplier",
    )


def test_append_email_to_thread_new_mail():
    expected_data = [{"children": [], "details": "dummy_response", "id": "EM_1", "type": "ada"}]
    actual_data = append_email_to_thread(
        [],
        new_email_details="dummy_response",
        chat_history=[],
        id_prefix="EM_",
    )

    assert actual_data == expected_data


def test_append_email_to_thread():
    expected_data = [
        {
            "children": [
                {"children": [], "details": "dummy_response", "id": "EM_2", "type": "ada"},
            ],
            "details": "dummy_response",
            "id": "EM_1",
            "type": "ada",
        },
    ]
    actual_data = append_email_to_thread(
        [{"children": [], "details": "dummy_response", "id": "EM_1", "type": "ada"}],
        new_email_details="dummy_response",
        chat_history=[],
        id_prefix="EM_",
    )

    assert actual_data == expected_data


def test_append_email_to_thread_with_one_child():
    expected_data = [
        {
            "children": [
                {"children": [], "details": "dummy_response", "id": "EM_2", "type": "ada"},
                {"children": [], "details": "dummy_response", "id": "EM_3", "type": "ada"},
            ],
            "details": "dummy_response",
            "id": "EM_1",
            "type": "ada",
        },
    ]
    actual_data = append_email_to_thread(
        [
            {
                "children": [
                    {"children": [], "details": "dummy_response", "id": "EM_2", "type": "ada"},
                ],
                "details": "dummy_response",
                "id": "EM_1",
                "type": "ada",
            },
        ],
        new_email_details="dummy_response",
        chat_history=[],
        id_prefix="EM_",
    )

    assert actual_data == expected_data


def test_generate_email(input_data, mock_dependencies, pg_retriever_mock):
    (
        _,
        run_conversation_chat_mock,
        _,
        email_prompts_mock,
        _,
        fetch_insights_for_supplier_mock,
        get_samples_mock,
    ) = mock_dependencies
    (
        _,
        _,
        _,
        chat_history,
        supplier_name,
        _,
        _,
        selected_elements,
    ) = input_data
    fetch_insights_for_supplier_mock.return_value = [
        {
            "insight": "test_insight",
            "insight_objective": "test objective type",
        },
    ]
    get_samples_mock.return_value = [{"example": "test sample"}]
    response = {"generation": """{"emails": "dummy_response"}"""}
    run_conversation_chat_mock.return_value = response
    email_prompts_mock.return_value = "test prompt"
    pg_retriever_mock.invoke.return_value = "test response"
    actual_response = generate_email(
        supplier_name,
        ["negotiation_objective_description"],
        "generate email",
        {
            "objectives": [
                {"objective": "test objective", "objective_type": "test objective type"},
            ],
            "supplier_profile": {"supplier_name": "test_supplier_name"},
        },
        chat_history,
        selected_elements,
        [],
        pg_db_conn=MagicMock(),
    )
    assert actual_response == {"emails": "dummy_response"}
