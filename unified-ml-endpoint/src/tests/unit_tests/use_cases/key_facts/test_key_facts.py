"""Tests for Key facts model workflow"""

import json
from unittest.mock import MagicMock, patch

import pytest

from ada.use_cases.key_facts.key_facts_v3 import (
    Configuration,
    PGConnector,
    generate_dax_query,
    get_formatted_output,
    key_facts_config,
    run_key_facts,
    summarize_dax_output,
)


@patch("ada.use_cases.key_facts.key_facts_v3.generate_dax_one_prompt")
@patch("ada.use_cases.key_facts.key_facts_v3.generate_chat_response_with_chain")
def test_generate_dax_query(mock_chat_response, mock_generate_dax_one_prompt):
    user_query = "Give me the category spend for last year?"
    few_shot_examples = {
        "few_shot_questions": ["few shot q1", "few shot q2", "few shot q3"],
        "few_shot_query_filtered": ["few shot query 1", "few shot query 2", "few shot query 3"],
    }
    category = "Bearings"

    configuration_dict = {
        "data_model": "mock data model",
        "measures_description": "mock measures description",
        "filters_description": "mock filters description",
        "category_filter": "{'level': 2, 'filter': 'mock filter level'}",
    }

    category_configuration = MagicMock()
    category_configuration.configuration_dict = configuration_dict

    mock_generate_dax_one_prompt.return_value = "expected prompt"
    mock_chat_response.return_value = "expected DAX query"

    result = generate_dax_query(user_query, few_shot_examples, category, category_configuration)

    # assertions
    assert result == "expected DAX query"

    mock_generate_dax_one_prompt.assert_called_once_with(
        data_model="mock data model",
        measure_description="mock measures description",
        filters_description="mock filters description",
        few_shot_questions=["few shot q1", "few shot q2", "few shot q3"],
        few_shot_query_filtered=["few shot query 1", "few shot query 2", "few shot query 3"],
        category=category,
        user_question=user_query,
        category_filter_level="mock filter level",
    )

    mock_chat_response.assert_called_once_with(
        prompt="expected prompt",
        model=key_facts_config["common_config"]["model"]["model_name"],
    )


@patch("ada.use_cases.key_facts.key_facts_v3.dax_response_generation_prompt")
@patch("ada.use_cases.key_facts.key_facts_v3.generate_chat_response_with_chain")
def test_summarize_dax_output(mock_generate_chat_response, mock_dax_response_generation_prompt):
    dax_output = '[{"column1": 1, "column2": 2}, {"column1": 3, "column2": 4}]'
    question = "example question"
    category = "example category"
    output_format = "json"

    mock_dax_response_generation_prompt.return_value = "expected summarization prompt"
    mock_generate_chat_response.return_value = "expected summarized response"

    result = summarize_dax_output(dax_output, question, category, output_format)

    # Assertions
    assert result == "expected summarized response"

    mock_generate_chat_response.assert_called_once_with(
        "expected summarization prompt",
        model=key_facts_config["common_config"]["model"]["model_name"],
    )


@patch("ada.use_cases.key_facts.key_facts_v3.dax_response_generation_prompt")
@patch("ada.use_cases.key_facts.key_facts_v3.generate_chat_response_with_chain")
def test_summarize_dax_output_invalid_json(
    mock_generate_chat_response,
    mock_dax_response_generation_prompt,
):
    dax_output = "invalid json"
    question = "example question"
    category = "example category"
    currency = "USD"

    mock_dax_response_generation_prompt.return_value = "expected prompt"
    mock_generate_chat_response.return_value = "expected DAX response"

    result = summarize_dax_output(dax_output, question, category, currency)

    # Assert that the result is as expected
    assert result == "expected DAX response"

    mock_dax_response_generation_prompt.assert_called_once_with(
        question=question,
        category=category,
        preferred_currency=currency,
        query_result_head=dax_output,
        query_result_tail=None,
    )

    mock_generate_chat_response.assert_called_once_with(
        "expected prompt",
        model=key_facts_config["common_config"]["model"]["model_name"],
    )


# TODO: Tests for get_report_details to be added after
#  we update the method in Phase 2 latency changes


@pytest.mark.parametrize(
    "message, query_title, report_id, additional_msg, expected_output",
    [
        (
            "Mock message 1",
            "",
            "",
            "",
            {
                "response_type": "summary",
                "response_prerequisite": "",
                "owner": "ai",
                "message": "Mock message 1",
                "links": [],
                "additional_text": "",
            },
        ),
        (
            None,
            "Spend",
            "123",
            "Here is a dashboard to enhance your understanding ",
            {
                "response_type": "summary",
                "response_prerequisite": "",
                "owner": "ai",
                "message": "",
                "links": [
                    {
                        "type": "powerBI",
                        "details": {
                            "title": "Key facts - Spend Dashboard",
                            "description": "Spend dashboard provides important data points that can help understand an organization's spend patterns.",  # noqa
                            "reportName": "TechCME Detailed Dashboard V1",
                            "pageName": "123",
                        },
                    },
                ],
                "additional_text": "Here is a dashboard to enhance your understanding on spend.",
            },
        ),
    ],
)
def test_get_formatted_output(message, query_title, report_id, additional_msg, expected_output):
    result = get_formatted_output(
        message=message,
        query_title=query_title,
        report_id=report_id,
        additional_msg=additional_msg,
    )
    assert result == expected_output


@pytest.mark.skipif(True, reason="Skipping due to dependency issue")
@patch("ada.use_cases.key_facts.key_facts_v3.exception_response")
@patch("ada.use_cases.key_facts.key_facts_v3.PGConnector")
@patch("ada.use_cases.key_facts.key_facts_v3.generate_embeddings_from_string")
@patch("ada.use_cases.key_facts.key_facts_v3.enhance_dax_query")
@patch("ada.use_cases.key_facts.key_facts_v3.generate_dax_query")
@patch("ada.use_cases.key_facts.key_facts_v3.summarize_dax_output")
@patch("ada.use_cases.key_facts.key_facts_v3.get_report_details")
@patch("ada.use_cases.key_facts.key_facts_v3.get_formatted_output")
def test_run_key_facts(
    mock_get_formatted_output,
    mock_get_report_details,
    mock_summarize_dax_output,
    mock_generate_dax_query,
    mock_enhance_dax_query,
    mock_generate_embeddings,
    mock_pg_connector_class,
    mock_exception_response,
):
    # setup pre-requisites
    mock_pg_connector = MagicMock(spec=PGConnector)
    mock_pg_connector_class.return_value = mock_pg_connector
    mock_pg_connector.search_by_vector_similarity.return_value = [
        (
            "some_category",
            "user_question",
            "[0.1,0.2,0.3]",
            "dax_query",
            0.2,
        ),
    ]

    mock_generate_embeddings.return_value = [0.1, 0.2, 0.3]
    mock_generate_dax_query.return_value = "Expected DAX query"
    mock_enhance_dax_query.return_value = "Expected enhanced DAX query"
    mock_summarize_dax_output.return_value = "Expected Summarized response"
    mock_get_report_details.return_value = {"report_id": "report_123", "title": "Report Title"}
    mock_get_formatted_output.return_value = {"message": "Formatted output"}

    mock_category_configuration = MagicMock(spec=Configuration)
    mock_category_configuration.load_configuration = MagicMock()
    mock_category_configuration.configuration_dict = {"currency": "{'currency': 'EUR'}"}

    # sample payload dict
    sample_payload_dict = {
        "dax_response_code": None,
        "user_query": "Sample_query",
        "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
        "request_id": "Sample_request",
        "category": "some_category",
    }

    # Test for category not supported
    mock_category_configuration.get_supported_categories.return_value = []
    mock_exception_response.return_value = {"error": "Category Error"}
    sample_json = json.dumps(sample_payload_dict)
    category = sample_payload_dict["category"]
    response = run_key_facts(sample_json, mock_category_configuration)
    assert response == {"error": "Category Error"}
    mock_exception_response.assert_called_with(
        response_type="exception",
        message=f"Selected category {category} is not supported by ada.\
            Please select another category to proceed.",
    )

    # sample payload dict
    sample_payload_dict = {
        "dax_response_code": None,
        "user_query": "Sample_query",
        "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
        "request_id": "Sample_request",
        "category": "Bearings",
    }

    # Test dax_response_code 400
    mock_category_configuration.get_supported_categories.return_value = ["Bearings"]
    mock_exception_response.return_value = {"error": "400 error"}
    sample_payload_dict["dax_response_code"] = 400
    sample_json = json.dumps(sample_payload_dict)
    response = run_key_facts(sample_json, mock_category_configuration)
    assert response == {"error": "400 error"}
    mock_exception_response.assert_called_with(
        response_type="exception",
        message="Ada was unable to answer this question, "
        "can you rephrase the question or be more specific?",
    )

    # Test dax_response_code 403
    mock_exception_response.return_value = {"error": "403 error"}
    sample_payload_dict["dax_response_code"] = 403
    sample_json = json.dumps(sample_payload_dict)
    response = run_key_facts(sample_json, mock_category_configuration)
    assert response == {"error": "403 error"}
    mock_exception_response.assert_called_with(
        response_type="exception",
        message="Sorry, Ada wasn't be able to access the database now. Please try later!",
    )

    # Test dax_response_code is not 200
    mock_exception_response.return_value = {"error": "Some error"}
    sample_payload_dict["dax_response_code"] = 500
    sample_json = json.dumps(sample_payload_dict)
    response = run_key_facts(sample_json, mock_category_configuration)
    assert response == {"error": "Some error"}
    mock_exception_response.assert_called_with(
        response_type="exception",
        message="Sorry, Ada wasn't able to answer this question for now.",
    )

    # Test dax_response_code None and exact match not found
    with patch.dict(
        "ada.use_cases.key_facts.key_facts_v3.key_facts_config",
        {
            "distance_threshold": 0.015,
            "dax_query_view_columns": [
                "request_id",
                "user_category",
                "user_question",
                "user_question_emb",
                "dax_query",
                "dax_query_custom_filters",
                "execution_status",
            ],
            "supported_categories": ["Bearings"],
        },
    ):
        sample_payload_dict["dax_response_code"] = None
        sample_json = json.dumps(sample_payload_dict)
        response = run_key_facts(sample_json, mock_category_configuration)

        assert response == {
            "response_type": "dax",
            "response_prerequisite": "Expected enhanced DAX query",
            "owner": "ai",
            "additional_text": "",
            "message": "",
            "links": [],
        }

        # Test dax_response_code 200
        sample_payload_dict["dax_response_code"] = 200
        sample_payload_dict["dax_response"] = {"example_key": "example_value"}
        sample_json = json.dumps(sample_payload_dict)
        response = run_key_facts(sample_json, mock_category_configuration)

        assert response == {"message": "Formatted output"}
