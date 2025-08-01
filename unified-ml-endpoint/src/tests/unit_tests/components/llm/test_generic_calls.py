"""Tests for generic components for LLM calls"""

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage

from ada.components.llm_models.generic_calls import (
    generate_embeddings_from_string,
    run_conversation_chat,
)


@patch("ada.components.llm_models.generic_calls.openai")
def test_generate_embeddings_from_string(mock_openai):
    mock_openai.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.1, 0.2, 0.3, 0.4])],
    )
    text = "Test input"
    model = "text-embedding-ada-002"
    embeddings = generate_embeddings_from_string(text, model)
    assert embeddings == [0.1, 0.2, 0.3, 0.4]
    mock_openai.embeddings.create.assert_called_once_with(
        input=text,
        model=model,
        extra_headers={"X-Aigateway-User-Defined-Tag": "NA-NA"},
    )


@patch("ada.components.llm_models.generic_calls.create_conversation_chain")
def test_run_conversation_chat_when_no_previous_history(
    create_conversation_chain_mock,
):
    prompt = MagicMock()
    input_str = "test input string"

    conversation_chain_mock = MagicMock()
    create_conversation_chain_mock.return_value = conversation_chain_mock
    conversation_chain_mock.invoke.return_value = AIMessage(content="test_response")

    expected_data = "test_response"
    actual_data = run_conversation_chat(
        [],
        prompt,
        input_str,
        model="gpt-4o",
        window_size=3,
        memory_type="window",
        temperature=0,
        input_message_key="input",
        history_message_key="history",
        session_id="",
    )

    assert expected_data == actual_data
    create_conversation_chain_mock.assert_called_with(
        model="gpt-4o",
        prompt=prompt,
        temperature=0.0,
        input_message_key="input",
        history_message_key="history",
    )
    conversation_chain_mock.invoke.assert_called_with(
        {"input": input_str},
        config={
            "configurable": {
                "chat_history_from_db": [],
                "memory_type": "window",
                "model": "gpt-4o",
                "session_id": "",
                "temperature": 0.0,
                "window_size": 3,
            },
        },
    )


@patch("ada.components.llm_models.generic_calls.create_conversation_chain")
def test_run_conversation_chat_with_previous_history(
    create_conversation_chain_mock,
):
    chat_history_from_db = MagicMock()
    prompt = MagicMock()
    input_str = "test input string"

    conversation_chain_mock = MagicMock()
    create_conversation_chain_mock.return_value = conversation_chain_mock
    conversation_chain_mock.invoke.return_value = AIMessage(content="test_response")

    expected_data = "test_response"
    actual_data = run_conversation_chat(
        chat_history_from_db,
        prompt,
        input_str,
        model="gpt-4o",
        window_size=3,
        memory_type="window",
        temperature=0,
        input_message_key="input",
        history_message_key="history",
        session_id="",
    )

    assert expected_data == actual_data
    create_conversation_chain_mock.assert_called_with(
        model="gpt-4o",
        prompt=prompt,
        temperature=0.0,
        input_message_key="input",
        history_message_key="history",
    )
    conversation_chain_mock.invoke.assert_called_with(
        {"input": input_str},
        config={
            "configurable": {
                "chat_history_from_db": chat_history_from_db,
                "memory_type": "window",
                "model": "gpt-4o",
                "session_id": "",
                "temperature": 0.0,
                "window_size": 3,
            },
        },
    )
