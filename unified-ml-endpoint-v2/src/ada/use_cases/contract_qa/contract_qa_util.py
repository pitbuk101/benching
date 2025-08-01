"""This contains utility functions for the contract QA use case."""

from typing import Any, Optional

import pandas as pd
from langchain_core.output_parsers import JsonOutputParser
from transformers import Pipeline

from ada.components.azureml.pipeline_steps import predict
from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.document_qna import (
    answer_is_helpful,
    ask_document_question,
)
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.components.llm_models.model_base import Model
from ada.components.prompts.prompts import (
    doc_clause_match_prompt,
    doc_info_answer_prompt,
)
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("contract_qna")
contract_qa_config = read_config("use-cases.yml")["contract_qna"]


def get_question_type(
    question_classifier_model: Pipeline,
    question: str,
    **kwargs: Any,
) -> str:
    """
    Get the question type based on single document question types such as "Extracted clause",
    "Extracted entity", "Non-extracted entity or clause", or "Multi-contract".
    Args:
        question_classifier_model (Pipeline): Trained classifier model to predict question type.
        question (str): User question.
        kwargs (Any): Additional keyword arguments.
    Returns:
        str: Question type based on the contract question classifier."""
    log.info("------ question classifier workflow selected ------ additional args %d", len(kwargs))
    predicted_class = predict(question_classifier_model, pd.Series([question]))[0]
    log.info("Question: %s \n Predicted class: %s", question, predicted_class)
    return predicted_class


def create_entity_dict(df_doc_info: pd.DataFrame) -> dict[str, Any]:
    """
    Club all the entities in to single dictionary

    Args:
        df_doc_info (pd.DataFrame): document info containing entity as column or as extracted entity
        dictionary column
    Returns:
        dict[str, Any]: A dictionary containing all entities, where the keys represent entity names,
    and the values are the corresponding extractions from the document or basic document information
    """
    data = df_doc_info.to_dict(orient="records")[0]
    entities = {key: value for key, value in data.items() if not isinstance(value, dict)}
    update_val = {
        i: j for _, value in data.items() if isinstance(value, dict) for i, j in value.items()
    }
    entities.update(update_val)
    return entities


def get_extracted_entities(doc_id: int, tenant_id: str) -> dict[str, Any]:
    """
    Get extracted entities for given document ID
    Args:
        doc_id (int): Document ID
        tenant_id (str): Tenant ID
    Returns:
        dict[str, Any]: A dictionary containing all entities, where the keys represent entity names,
    and the values are the corresponding extractions from the document or basic document information
    """
    columns = ["region", "supplier", "sku", "entity_extraction"]
    df_doc_info = PGConnector(tenant_id=tenant_id).get_data_for_document_from_table(
        "contract_details",
        columns,
        doc_id,
    )
    return create_entity_dict(df_doc_info)


def answer_entity_related_question(
    doc_id: int,
    tenant_id: str,
    question: str,
    **kwargs: Any,
) -> Optional[dict[str, Any]]:
    """
    Answer entity related question

    Args:
        doc_id (int): Document ID
        tenant_id (str): Tenant ID
        question (str): User question related to contract entity
        kwargs (Any): Additional keyword arguments
    Returns:
        Optional[dict[str, Any]]: A response from LLM for the given entity question if found;
                                otherwise, None.
    """
    log.info("------ extracted entity workflow selected ------%d", len(kwargs))
    doc_entities = get_extracted_entities(doc_id, tenant_id=tenant_id)
    log.info(doc_entities)
    prompt = doc_info_answer_prompt(question, doc_entities)
    answer = generate_chat_response_with_chain(
        prompt=prompt,
        model=contract_qa_config["model"]["openai_model_name"],
    )
    log.info(answer)
    if answer_is_helpful(question, answer, model=contract_qa_config["model"]["openai_model_name"]):
        return {
            "question": question,
            "answer": answer,
            "sources": "Extracted entities",
        }
    return None


def find_relevant_clause_to_question(
    question: str,
    df_doc_clauses: pd.DataFrame,
) -> dict[str, Any]:
    """
    Find the relevant clause to a given question from the document clause list.

    Args:
        question (str): User question
        df_doc_clauses (pd.DataFrame): Document clauses data

    Returns:
        Optional[dict[str, Any]]: A dictionary representing the relevant clause to the question
        if found; otherwise, None.
    """
    doc_clauses = df_doc_clauses["clauses"][0]
    prompt = doc_clause_match_prompt(question, doc_clauses)
    best_match_clause_result = generate_chat_response_with_chain(
        prompt=prompt,
        model=contract_qa_config["model"]["openai_model_name"],
        parser=JsonOutputParser(),
    )
    log.info(best_match_clause_result)
    if isinstance(best_match_clause_result, dict):
        return best_match_clause_result
    return {}


def answer_clauses_related_question(
    doc_id: int,
    tenant_id: str,
    question: str,
    df_doc_chunks: pd.DataFrame,
    model: Model,
    **kwargs: Any,
) -> Optional[dict[str, Any]]:
    """
    Run clauses QA.

    Args:
        doc_id (int): Document ID
        tenant_id (str): Tenant ID
        question (str): User question related to contract clauses
        df_doc_chunks (pd.DataFrame): Document chunk data
        model (Model): LLM model object
        kwargs (Any): Additional keyword arguments
    Returns:
        Optional[dict[str, Any]]: A response from LLM for the given clause question if found;
                                otherwise, None.
    """
    log.info("----- extracted clauses workflow selected -----%d", len(kwargs))
    columns = ["clauses"]
    df_doc_clauses = PGConnector(tenant_id=tenant_id).get_data_for_document_from_table(
        "contract_details",
        columns,
        doc_id,
    )
    relevant_clause = find_relevant_clause_to_question(question, df_doc_clauses)
    answer = "We were unable to find the answer you are looking for,\
                 as the document doesn't have details about the clause you asked."
    answer = (
        answer
        if relevant_clause.get("Answer", "NO").upper() == "NO"
        else relevant_clause.get("Answer", "")
    )
    if relevant_clause.get("Most Similar Sections", ""):
        doc_chunks = df_doc_chunks[
            df_doc_chunks["chunk_id"].isin(relevant_clause.get("Most Similar Sections", ""))
        ]
        clauses_vectorstore = VectorStoreFactory().faiss_from_embeddings(doc_chunk=doc_chunks)
        response = ask_document_question(
            question,
            clauses_vectorstore,
            search_k=contract_qa_config["clause_retriever_search_k"],
            model=model,
            model_host=model.model_host,
        )
        answer = response.get("answer", "")
        if answer_is_helpful(question, answer, model=model.model_name):
            return {
                "question": question,
                "answer": answer,
                "sources": "Extracted clauses",
            }

    return {
        "question": question,
        "answer": answer,
        "sources": "Extracted clauses",
    }


def answer_regular_questions(**params: Any) -> dict[str, Any]:
    """
    Answers regular questions based on the provided parameters.

    Args:
        params (Any): A dictionary containing the parameters
        required to answer the question.
    Returns:
        dict[str, Any]: A dictionary containing the answer to the question.
    """
    response = ask_document_question(**params).get("answer", "")
    return {
        "question": params.get("question", ""),
        "answer": response,
        "sources": "regular doc qna",
    }


def is_integer(value: str | Any) -> bool:
    """
    Check if the given value can be converted to an integer.

    Parameters:
    - value (str or any): The value to check.

    Returns:
    - bool: True if the value can be converted to an integer, False otherwise.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
