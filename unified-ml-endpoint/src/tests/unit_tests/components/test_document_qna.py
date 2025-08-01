from unittest.mock import ANY, MagicMock, patch

from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever

from ada.components.llm_models.document_qna import (
    ask_document_question_v2,
    extract_links,
)
from ada.components.llm_models.model_base import Model
from ada.use_cases.source_ai_knowledge.source_ai_knowledge import source_ai_conf


def test_extract_links():
    llm_response = (
        "you can refer this site for reference:[Google](https://google.com/maps) and [OpenAI]("
        "https://openai.com/index/sora)"
    )
    ans, links = extract_links(llm_response)
    assert ans == "you can refer this site for reference:Google and OpenAI"
    assert links == [
        {"type": "source_ai", "details": {"title": "Maps", "link": "https://google.com/maps"}},
        {
            "type": "source_ai",
            "details": {
                "title": "Sora",
                "link": "https://openai.com/index/sora",
            },
        },
    ]


def test_extract_links_without_link():
    llm_response = "You can generate ideas in the Idea Sandbox Insights and Negotiation Factory sections of SourceAI"
    ans, links = extract_links(llm_response)
    assert ans == llm_response
    assert links == []


@patch("ada.components.llm_models.document_qna.answer_is_helpful")
@patch("ada.components.llm_models.document_qna.run_qa_chain")
@patch("ada.components.llm_models.document_qna.create_qa_chain")
@patch("ada.components.llm_models.document_qna.extract_links")
def test_ask_document_question_v2_with_ans(
    extract_links_mock,
    create_qa_chain_mock,
    run_qa_chain_mock,
    answer_is_helpful_mock,
):
    question = "Where can I generate ideas?"
    answer = "You can generate ideas in the Idea Sandbox Insights on SourceAI."

    vectorstore = MagicMock(spec=FAISS)
    retriever = MagicMock(spec=VectorStoreRetriever)
    vectorstore.as_retriever.return_value = retriever

    chain = MagicMock()
    create_qa_chain_mock.return_value = chain

    run_qa_chain_mock.return_value = {"answer": answer}
    extract_links_mock.return_value = (answer, [])
    answer_is_helpful_mock.return_value = True

    model = Model(name=source_ai_conf["model"]["rag_model_name"])
    result = ask_document_question_v2(
        question=question,
        vectorstore=vectorstore,
        search_k=5,
        include_sources=False,
        model=model.model_name,
        model_host=model.model_host,
        temperature=0.7,
    )
    answer_is_helpful_mock.assert_called_once_with(question, answer, model=model.model_name)

    create_qa_chain_mock.assert_called_once_with(
        retriever=retriever,
        prompt=ANY,
        model=model.model_name,
        temperature=0.7,
        return_sources=True,
    )

    run_qa_chain_mock.assert_called_once_with(chain, question)
    extract_links_mock.assert_called_once_with(answer)

    assert result == {"answer": answer, "links": []}


@patch("ada.components.llm_models.document_qna.answer_is_helpful")
@patch("ada.components.llm_models.document_qna.run_qa_chain")
@patch("ada.components.llm_models.document_qna.create_qa_chain")
@patch("ada.components.llm_models.document_qna.extract_links")
def test_ask_document_question_v2_with_no_ans(
    extract_links_mock,
    create_qa_chain_mock,
    run_qa_chain_mock,
    answer_is_helpful_mock,
):
    question = "Where can I generate ideas?"
    answer = "You can generate ideas in the Idea Sandbox Insights on SourceAI."

    vectorstore = MagicMock(spec=FAISS)
    retriever = MagicMock(spec=VectorStoreRetriever)
    vectorstore.as_retriever.return_value = retriever

    chain = MagicMock()
    create_qa_chain_mock.return_value = chain

    run_qa_chain_mock.return_value = {"answer": answer}
    extract_links_mock.return_value = (answer, [])
    answer_is_helpful_mock.return_value = False

    model = Model(name=source_ai_conf["model"]["rag_model_name"])
    result = ask_document_question_v2(
        question=question,
        vectorstore=vectorstore,
        search_k=5,
        include_sources=False,
        model=model.model_name,
        model_host=model.model_host,
        temperature=0.7,
    )
    answer_is_helpful_mock.assert_called_once_with(question, answer, model=model.model_name)

    create_qa_chain_mock.assert_called_once_with(
        retriever=retriever,
        prompt=ANY,
        model=model.model_name,
        temperature=0.7,
        return_sources=True,
    )
    run_qa_chain_mock.assert_called_once_with(chain, question)

    assert result == {"answer": "answer not found", "sources": ""}
    extract_links_mock.assert_not_called()
