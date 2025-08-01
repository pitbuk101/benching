"""
Entity extraction for benchmarking component for batch pipeline
"""

import json
from typing import Any, Collection

import pandas as pd
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore

from ada.components.llm_models.generic_calls import (
    generate_qa_chain_response_with_sources,
)
from ada.components.llm_models.model_base import Model
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.benchmarking.calls import process_data_extractor_response
from ada.use_cases.benchmarking.prompts import factual_data_prompt, merge_data_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.format.format import replace_dict_str_to_json_str
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.context_manager import (
    UseCase,
    set_tenant_and_intent_flow_context,
)

log = get_logger("benchmarking")

config = read_config("use-cases.yml")["benchmarking"]


def extract_factors(data_frame: pd.DataFrame, condition: str | Any) -> str:
    """
    Extract factors from a DataFrame based on a given condition.
    Args:
        data_frame (pd.DataFrame): The DataFrame to extract factors from.
        condition (str or callable): The condition to filter factors.
    Returns:
        str: A list of factors that match the condition.
    """
    filtered_data = data_frame.loc[
        data_frame["Qualitative or quantitative?"] == condition,
        "index_and_description",
    ]
    factors_list = filtered_data.to_list()
    factors_string = ", ".join(factors_list)
    return factors_string


def import_csv_sheet_for_term_extraction(question_file: str) -> list[str]:
    """
    Import data from a CSV file and extract numerical and trend factors.
    Args:
        question_file (str): Path to the CSV file containing data.
    Returns:
        (list[str]): A tuple containing two lists - numerical factors and trend factors.
    """
    df_questions = pd.read_csv(question_file, header=0)
    df_questions["index_and_description"] = df_questions["Benchmark"].astype(str)
    numerical_factors = extract_factors(df_questions, "Quantitative")
    trend_factors = extract_factors(df_questions, "Qualitative")
    return [numerical_factors, trend_factors]


def query_llm_model(
    model: BaseLanguageModel,
    prompt: PromptTemplate,
    question: str,
    output_format: str = "",
) -> dict[str, str]:
    """
    Run a general LLM chain.
    Args:
        model (BaseLanguageModel): selected model.
        prompt (PromptTemplate): Input script of the prompt.
        question (str): question for the LLM.
        output_format (str): output format of response.
    Returns:
        (dict[str, str]) response from LLM chain
    """
    merge_chain = prompt | model | JsonOutputParser()
    final_resp = merge_chain.invoke({"information": question, "output_format": output_format})
    return final_resp


def query_llm_entity_extraction(
    model: BaseLanguageModel,
    vectorstore: VectorStore,
    prompt: PromptTemplate,
    question: str,
) -> dict[str, str | Collection[str]]:
    """Run an entity extraction chain.

    Args:
        model (BaseLanguageModel): selected model
        vectorstore (VectorStore): vectorstore from embeddings and chunks
        prompt (PromptTemplate): Input script of the prompt
        question (str): question for the LLM.
        output_format (str): output format of response
    Returns:
        (dict[str, str| Collection[str]]): response from LLM chain
    Raises:
        ValueError("VectorStore object does not exist") when the vectorstore
        does not exist
    """
    if not vectorstore:
        raise ValueError("VectorStore object does not exist")
    response = generate_qa_chain_response_with_sources(
        user_query=question,
        retriever=vectorstore.as_retriever(),
        prompt=prompt,
        model=model,
    )
    processed_response = process_data_extractor_response(response)
    return processed_response


def generate_output_format(factors: str) -> str:
    """
    Generate a JSON object from a comma-separated list of factors.
    Args:
        factors (str): Comma-separated list of factors.
    Returns:
        (str) : A string dictionary with factors as keys and empty string values.
    """
    factor_list = [factor.strip() for factor in factors.split(",")]
    output_format = ",\n".join([f'"{factor}": ""' for factor in factor_list])
    return "{" + output_format + "}"


def extract_entities(vector_store: VectorStore) -> dict[str, str | Collection[Any]]:
    """
    Extract entities from document
    Args:
        vector_store (VectorStore): Vectorstore of the document
    Returns:
        (dict[str, str | Collection[Any]]): The entities and their sources for benchmarking
    """
    numerical_questions, _ = import_csv_sheet_for_term_extraction(config["csv_for_benchmark"])
    model = Model(name=config["model"]).obj
    numerical_factor_dictionary = json.loads(generate_output_format(numerical_questions))
    numerical_factor_response = query_llm_entity_extraction(
        model=model,
        vectorstore=vector_store,
        prompt=factual_data_prompt(),
        question=numerical_questions,
    )
    merged_factors = query_llm_model(
        model=model,
        prompt=merge_data_prompt(),
        question=str(numerical_factor_response["answer"]),
        output_format=str({**numerical_factor_dictionary}),
    )
    entity_extraction_result = {
        "answer": merged_factors,
        "sources": [replace_dict_str_to_json_str(str({**numerical_factor_response}["source"]))],
    }
    log.info("Benchmarking entity extraction results: \n %s", entity_extraction_result)
    log.info("Entity extracted successfully for benchmarking")
    return entity_extraction_result


def run_benchmarking(
    df_doc_chunks: pd.DataFrame,
    tenant_id: str,
) -> dict[str, str | Collection[Any]]:
    """
    Run benchmarking
    Args:
        df_doc_chunks (pd.DataFrame): DataFrame containing document chunks
    Returns:
        (dict[str, str | Collection[Any]]): The entities and their sources for benchmarking
    """
    set_tenant_and_intent_flow_context(tenant_id, UseCase.CONTRACT_BENCHMARKING)
    log.info("Initializing Benchmarking")
    vector_store_factory = VectorStoreFactory()
    vectorstore = vector_store_factory.faiss_from_embeddings(doc_chunk=df_doc_chunks)
    result = extract_entities(vectorstore)
    log.info("COMPLETED: Benchmarking")
    return result
