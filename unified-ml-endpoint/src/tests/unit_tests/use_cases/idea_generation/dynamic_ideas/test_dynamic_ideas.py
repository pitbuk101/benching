import json
from unittest.mock import MagicMock, patch

import pytest

from ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas import (
    create_langgraph,
    run_dynamic_ideas_graph,
)
from ada.use_cases.idea_generation.exception import DynamicQnAException


@patch("ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas.create_langgraph")
def test_run_dynamic_ideas_graph(mock_create_langgraph):
    """Test run_dynamic_ideas_graph with valid inputs."""

    mock_create_langgraph.return_value.invoke.return_value = {
        "response_payload": {"result": "success"},
    }
    mock_pg_db_conn = MagicMock()
    chat_history = ["Hello", "What are the top ideas?"]
    valid_json_str = json.dumps(
        {
            "user_query": "What are the top ideas?",
            "request_type": "user_input",
            "page_id": "ada-home",
            "category": "bearings",
            "tenant_id": "tenant123",
        },
    )

    response = run_dynamic_ideas_graph(valid_json_str, chat_history, mock_pg_db_conn)
    mock_create_langgraph.return_value.invoke.assert_called_once_with(
        {
            "chat_history": chat_history,
            "pg_db_conn": mock_pg_db_conn,
            "user_query": "What are the top ideas?",
            "request_type": "user_input",
            "page_id": "ada-home",
            "category": "bearings",
            "tenant_id": "tenant123",
        },
    )

    assert response == {"result": "success"}


@patch("ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas.create_langgraph")
def test_run_dynamic_ideas_graph_invalid_inputs(mock_create_langgraph):
    """Test run_dynamic_ideas_graph with invalid inputs."""
    mock_create_langgraph.return_value.invoke.return_value = {
        "response_payload": {"result": "success"},
    }
    mock_pg_db_conn = MagicMock()
    chat_history = ["Hello", "What are the top ideas?"]

    # Scenario 1: Unsupported page_id
    invalid_json_str_invalid_page_id = json.dumps(
        {
            "user_query": "What are the top ideas?",
            "request_type": "user_input",
            "page_id": "unsupported-page",
            "category": "bearings",
            "tenant_id": "tenant123",
        },
    )

    with pytest.raises(DynamicQnAException) as exc_info:
        run_dynamic_ideas_graph(invalid_json_str_invalid_page_id, chat_history, mock_pg_db_conn)

    assert "Unsupported 'page_id'" in str(exc_info.value)

    # Scenario 2: Missing required field in JSON (e.g., tenant_id)
    missing_input_json = json.dumps(
        {
            "user_query": "What are the top ideas?",
            "request_type": "user_input",
            "page_id": "ada-home",
            "category": "bearings",
        },
    )

    with pytest.raises(DynamicQnAException) as exc_info:
        run_dynamic_ideas_graph(missing_input_json, chat_history, mock_pg_db_conn)

    assert "validation error for RequestPayload" in str(exc_info.value)


def test_create_langgraph_no_exception():
    """Test that create_langgraph does not raise any exceptions."""
    try:
        workflow = create_langgraph()
        assert workflow is not None, "The workflow should be successfully created and compiled."
    except Exception as e:
        pytest.fail(f"create_langgraph raised an exception: {e}")
