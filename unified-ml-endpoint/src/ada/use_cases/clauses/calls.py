"""Calls used in the clauses QnA use case."""

from typing import Any

from langchain_core.documents import Document

from ada.components.llm_models.generic_calls import run_qa_chain


def generate_clause_qa_response(chain: Any, question: str) -> tuple[str, list[Document]]:
    """
    Query the LLM to get the answer about a clause

    Args:
        chain (Any): langchain QA object
        question (str): question about the clause

    Returns:
        Query result (YES/NO) and the full explanation
    """

    response = run_qa_chain(chain, question)
    if response.get("answer", "").startswith("YES"):
        result = "YES"
    elif response.get("answer", "").startswith("NO"):
        result = "NO"
    else:
        result = "NA"
    return result, response.get("context", [])
