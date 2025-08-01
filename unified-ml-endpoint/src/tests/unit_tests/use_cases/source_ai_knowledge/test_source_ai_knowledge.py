import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from langchain_community.chat_message_histories import ChatMessageHistory

from ada.use_cases.source_ai_knowledge.exception import SourceAIKnowledgeException
from ada.use_cases.source_ai_knowledge.source_ai_knowledge import (
    run_source_ai_knowledge,
)


@pytest.fixture
def mock_dependencies():
    with (
        patch(
            "ada.use_cases.source_ai_knowledge.tools.doc_summary_qa_tool.generate_chat_response_with_chain",
        ) as generate_chat_response_mock,
        patch(
            "ada.use_cases.source_ai_knowledge.source_ai_knowledge.generate_conversational_rag_agent_response",
        ) as generate_conversational_rag_response_mock,
        patch(
            "ada.use_cases.source_ai_knowledge.source_ai_knowledge.PGRetriever",
        ) as pg_db_conn_mock,
    ):
        yield (
            generate_chat_response_mock,
            generate_conversational_rag_response_mock,
            pg_db_conn_mock,
        )


def test_run_source_ai_knowledge_wrong_intent():
    """Test sourceAI bot."""
    input_json = {
        "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
        "intent": "",
        "user_input": "How do we negotiate with supplier based on insights?",
        "category": "Bearings",
    }
    chat_history = ChatMessageHistory(messages=[])

    with pytest.raises(SourceAIKnowledgeException) as excinfo:
        run_source_ai_knowledge(
            json.dumps(input_json),
            chat_history,
            pg_db_conn=MagicMock(),
        )

    assert "intent retrieved from realtime params is not valid!" in str(excinfo.value)


def test_run_source_ai_knowledge(mock_dependencies):
    """Test sourceAI bot response from document references."""
    input_json = {
        "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
        "intent": "source ai knowledge",
        "user_input": "How do we negotiate with supplier based on insights?",
        "category": "Bearings",
    }
    answer = """To negotiate with a supplier based on insights, you first need to understand the supplier and
    the strategy to use during negotiation. This can be achieved through the Negotiation Factory tool,
    which provides a holistic understanding of the supplier"""

    chat_history = ChatMessageHistory(messages=[])

    data = {
        "page": [1],
        "embedding": [
            [
                -0.0069588246,
                -0.020910753,
                -0.03452674,
                -0.0080009345,
                -0.0072810557,
                0.015617933,
                -0.009673795,
                -0.02110272,
            ],
        ],
    }
    (
        _,
        generate_conversational_rag_response_mock,
        pg_db_conn_mock,
    ) = mock_dependencies

    generate_conversational_rag_response_mock.return_value = {"generation": answer}

    expected_data = {
        "result": answer,
        "links": [],
        "response_type": "source-ai-knowledge",
    }

    pg_db_conn_mock.return_value = pd.DataFrame(data)

    source_ai_response = run_source_ai_knowledge(
        json.dumps(input_json),
        chat_history,
        pg_db_conn_mock,
    )
    assert source_ai_response == expected_data


def test_run_source_ai_knowledge_with_gp(mock_dependencies):
    """Test sourceAI bot with general purpose bot."""
    input_json = {
        "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
        "intent": "source ai knowledge",
        "user_input": "what is the capital of India?",
        "category": "Bearings",
    }
    answer = "New Delhi"
    chat_history = ChatMessageHistory(messages=[])

    (
        _,
        generate_conversational_rag_response_mock,
        pg_db_conn_mock,
    ) = mock_dependencies

    expected_data = {"result": answer, "response_type": "procurement-knowledge"}
    pg_db_conn_mock.return_value = []

    generate_conversational_rag_response_mock.return_value = {
        "generation": {"result": answer, "response_type": "procurement-knowledge"},
    }

    source_ai_response = run_source_ai_knowledge(
        json.dumps(input_json),
        chat_history,
        pg_db_conn_mock,
    )

    assert source_ai_response == expected_data
