from unittest.mock import patch

import pytest

from ada.use_cases.idea_generation.idea_generation_utils import (
    IdeaGenException,
    generate_response_dict,
    generate_selected_idea_prompt_response,
    input_data_validation,
    model_config,
)


@patch("ada.use_cases.idea_generation.idea_generation_utils.get_selected_idea_prompt")
@patch("ada.use_cases.idea_generation.idea_generation_utils.generate_chat_response_with_chain")
def test_generate_selected_idea_prompt_response(mock_chat_response, mock_selected_idea_prompt):
    # test data
    retrieved_context = "retrieved_context"
    insight_context = "insight_context"
    pinned_elements = "pinned_elements"
    user_input = "user_input"
    selected_idea = "selected_idea"

    mock_selected_idea_prompt.return_value = "Test Prompt"
    mock_chat_response.return_value = "Test Response"

    result = generate_selected_idea_prompt_response(
        retrieved_context,
        insight_context,
        pinned_elements,
        user_input,
        selected_idea,
    )

    # assertions
    mock_selected_idea_prompt.assert_called_once_with(
        retrieved_context=retrieved_context,
        insight_context=insight_context,
        pinned_elements=pinned_elements,
        user_query=user_input,
        selected_idea=selected_idea,
    )

    mock_chat_response.assert_called_once_with(
        "Test Prompt",
        model=model_config["model_name"],
    )

    assert result == "Test Response"


@pytest.mark.parametrize(
    "chat_id, request_type",
    [
        ("valid_chat_id", "linked_insights"),
        ("valid_chat_id", "rca"),
        ("valid_chat_id", "ideas"),
        ("valid_chat_id", "user_input"),
        ("valid_chat_id", "clear_chat_history"),
    ],
)
@patch("ada.use_cases.idea_generation.idea_generation_utils.log")
def test_input_data_validation_valid(mock_log, chat_id, request_type):
    input_data_validation(chat_id, request_type)

    # Assertions
    mock_log.error.assert_not_called()
    mock_log.info.assert_any_call(
        "Chat ID retrieved from the realtime params : %s",
        chat_id,
    )
    mock_log.info.assert_any_call(
        "Request type retrieved from the realtime params : %s",
        request_type,
    )


@pytest.mark.parametrize("chat_id", [None, 123, {}])
@patch("ada.use_cases.idea_generation.idea_generation_utils.log")
def test_input_data_validation_invalid_chat_id(mock_log, chat_id):
    # Execute the function and assert exception
    with pytest.raises(IdeaGenException) as exc_info:
        input_data_validation(chat_id, "linked_insights")

    # Assertions
    assert (
        str(
            exc_info.value,
        )
        == "chat_id retrieved from realtime params is either None or not a string!"
    )
    mock_log.error.assert_called_once_with(
        "chat_id retrieved from realtime params is either None or not a string!",
    )


@patch("ada.use_cases.idea_generation.idea_generation_utils.log")
def test_input_data_validation_invalid_request_type(mock_log):
    # Execute the function and assert exception
    with pytest.raises(IdeaGenException) as exc_info:
        input_data_validation("valid_chat_id", "invalid_request_type")

    # Assertions
    assert (
        str(
            exc_info.value,
        )
        == "Invalid request_type retrieved from the realtime params: invalid_request_type"
    )
    mock_log.error.assert_called_once_with(
        "Invalid request_type retrieved from the realtime params: invalid_request_type",
    )


@pytest.mark.parametrize(
    "chat_id, response_type, rca_list, ideas_list, answer_str, linked_insights_list, expected_response",
    [
        (
            "test_chat_id",
            "test_response_type",
            None,
            None,
            None,
            None,
            {
                "chat_id": "test_chat_id",
                "response_type": "test_response_type",
                "response": {
                    "root_causes": [],
                    "ideas": [],
                    "answer": "",
                    "linked_insights": [],
                },
            },
        ),
        (
            "test_chat_id",
            "test_response_type",
            ["rca1", "rca2"],
            ["idea1", "idea2"],
            "chat model response",
            ["insight1", "insight2"],
            {
                "chat_id": "test_chat_id",
                "response_type": "test_response_type",
                "response": {
                    "root_causes": ["rca1", "rca2"],
                    "ideas": ["idea1", "idea2"],
                    "answer": "chat model response",
                    "linked_insights": ["insight1", "insight2"],
                },
            },
        ),
    ],
)
def test_generate_response_dict(
    chat_id,
    response_type,
    rca_list,
    ideas_list,
    answer_str,
    linked_insights_list,
    expected_response,
):
    result = generate_response_dict(
        chat_id,
        response_type,
        rca_list=rca_list,
        ideas_list=ideas_list,
        answer_str=answer_str,
        linked_insights_list=linked_insights_list,
    )

    # Assert
    assert result == expected_response
