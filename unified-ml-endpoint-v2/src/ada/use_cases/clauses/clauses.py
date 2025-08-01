""" Clauses component for batch pipeline """

import pathlib
from typing import Any

import pandas as pd
from openai import OpenAIError

from ada.components.llm_models.generic_calls import create_qa_chain
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.clauses.calls import generate_clause_qa_response
from ada.use_cases.clauses.prompts import retrieve_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.io.misc import import_csv_sheet_for_clauses
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.context_manager import (
    UseCase,
    set_tenant_and_intent_flow_context,
)

log = get_logger("clauses")


def run_clauses(df_doc_chunks: pd.DataFrame, tenant_id: str) -> list[dict[str, Any]]:
    """Run clauses.
    Args:
        df_doc_chunks (pd.DataFrame): DataFrame containing document chunks.
    Returns:
        list[dict[str, str]]: List of clauses
    """
    set_tenant_and_intent_flow_context(tenant_id, UseCase.CONTRACT_CLAUSES)
    log.info("Initializing Clauses")
    vector_store_factory = VectorStoreFactory()
    vector_store = vector_store_factory.faiss_from_embeddings(doc_chunk=df_doc_chunks)
    clause_config = read_config("use-cases.yml")["clauses"]
    model_config = clause_config["model"]
    question_file = clause_config["csv_for_checklist"]
    parent_dir = pathlib.Path(__file__).parents[4]
    que_file_dir = f"{parent_dir}/{question_file}"
    list_clauses, list_questions = import_csv_sheet_for_clauses(que_file_dir)

    retriever = vector_store.as_retriever(search_kwargs={"k": model_config["retriever_search_k"]})
    prompt = retrieve_prompt()
    chain = create_qa_chain(
        retriever=retriever,
        prompt=prompt,
        model=model_config["model_name"],
        temperature=model_config["temperature"],
        return_sources=True,
    )
    # This chain will be used if prompt is too long for the previous chain
    long_chain = create_qa_chain(
        retriever=retriever,
        prompt=prompt,
        model=model_config["long_model_name"],
        temperature=model_config["long_model_temperature"],
        return_sources=True,
    )

    list_results = []
    list_page_numbers = []
    for clause, question in zip(list_clauses, list_questions):
        log.info("Processing for clause: %s with question: %s ", clause, question)
        try:
            result, docs = generate_clause_qa_response(chain, question)
        except OpenAIError:
            result, docs = generate_clause_qa_response(long_chain, question)
        list_results.append(result)
        page_numbers = [doc.metadata["source"] for doc in docs]
        list_page_numbers.append(page_numbers)

    result_list = [
        {"Clause/section": clause, "Answer": result, "Most Similar Sections": page_numbers}
        for clause, result, page_numbers in zip(list_clauses, list_results, list_page_numbers)
    ]
    log.info("COMPLETED: clauses")
    return result_list
