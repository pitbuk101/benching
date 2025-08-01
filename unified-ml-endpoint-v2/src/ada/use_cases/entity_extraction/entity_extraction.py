"""
Entity extraction component for batch pipeline
"""

import time
from typing import Any

import pandas as pd
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore

from ada.components.llm_models.generic_calls import (
    generate_chat_response,
    generate_chat_response_with_chain,
    generate_qa_chain_response_without_sources,
)
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.entity_extraction.prompts import (
    descriptions_dict,
    get_chain_prompt,
    get_convenience_prompt,
    get_duration_prompt,
    get_pydantic_formatting_prompt,
    get_system_prompt,
)
from ada.use_cases.entity_extraction.pydantic_parsing import days_parser, months_parser
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.context_manager import (
    UseCase,
    set_tenant_and_intent_flow_context,
)

log = get_logger("entity_extraction")


def run_chat_model_entity_extraction(
    entity_name: str,
    vector_store: VectorStore,
    prompt: PromptTemplate,
    chat_config: dict[str, Any],
    output_parser: PydanticOutputParser,
    search_k: int = 4,
) -> str:
    """Run chat model output extraction.

    Args:
        entity_name (str): name of entity from descriptions_dict.
        vector_store (VectorStore): vectorstore used for document search.
        prompt (PromptTemplate): entity-specific prompt template.
        chat_config (dict): configuration for chat model.
        output_parser (PydanticOutputParser): pydantic output parser.
        search_k (int): number of similar documents to retrieve, default 4 as in langchain.

    Returns:
        (str): parsed output , int formatted as string in case value was found, NA otherwise.
    """
    t_start = time.time()

    selected_docs = vector_store.similarity_search(descriptions_dict[entity_name], k=search_k)
    doc_content = [doc.page_content for doc in selected_docs[::-1]]
    relevant_docs = "\n\n".join(doc_content)

    prompt = prompt.format_prompt(query=relevant_docs)
    message = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": prompt.to_string()},
    ]

    output = generate_chat_response(
        messages=message,
        model=chat_config["model_name"],
        temperature=chat_config["temperature"],
    )

    t_consumed = round(time.time() - t_start, 2)
    log.info("Entity %s chat extraction: %s, time consumed: %s", entity_name, output, t_consumed)

    return output_parser.parse(output).number


def run_chain_entity_extraction(
    entity_name: str,
    vector_store: VectorStore,
    chain_config: dict[str, Any],
    output_parser: PydanticOutputParser,
) -> str:
    """Run QA chain entity extraction.

    Args:
        entity_name (str): name of entity from descriptions_dict.
        vector_store (VectorStore): vectorstore used for document search.
        chain_config (dict): configuration for chain model.
        output_parser (PydanticOutputParser): pydantic output parser.

    Returns:
        (str): parsed output, int formatted as string in case value was found, NA otherwise.
    """
    t_start = time.time()
    entity_retriever = vector_store.as_retriever(
        search_type=chain_config["search_type"],
        search_kwargs=chain_config["search_kwargs"],
    )
    entity_prompt = get_chain_prompt(entity_name)
    entity_output = generate_qa_chain_response_without_sources(
        user_query=f"{entity_name}: {descriptions_dict[entity_name]}",
        retriever=entity_retriever,
        prompt=entity_prompt,
        model=chain_config["model_name"],
        temperature=chain_config["temperature"],
    )

    t_consumed = round(time.time() - t_start, 2)
    log.info("Entity %s extraction: %s, time consumed: %s", entity_name, entity_output, t_consumed)

    try:
        parsed_output = output_parser.parse(entity_output).number
    except OutputParserException:
        formatting_prompt = get_pydantic_formatting_prompt(output_parser)
        formatting_prompt = formatting_prompt.format_prompt(query=entity_output)
        entity_output = generate_chat_response_with_chain(
            prompt=formatting_prompt,
            model=chain_config["correction_model_name"],
            temperature=chain_config["correction_model_temperature"],
            response_format="json_object",
        )
        parsed_output = output_parser.parse(entity_output).number
    return parsed_output


def run_entity_extraction(df_doc_chunks: pd.DataFrame, tenant_id: str) -> dict[str, str]: # NOSONAR
    """
    Run entity extraction.
    Args:
        df_doc_chunks (pd.DataFrame): DataFrame containing document chunks.
    Returns:
        (dict[str, str]): Dictionary of the extracted entities
    """
    log.info("Initializing entity extraction prompts and models")
    t_ee_start = time.time()

    set_tenant_and_intent_flow_context(tenant_id, UseCase.CONTRACT_ENTITY_EXTRACTION)

    model_config = read_config("use-cases.yml")["entity_extraction"]

    vector_store_factory = VectorStoreFactory()
    vector_store = vector_store_factory.faiss_from_embeddings(doc_chunk=df_doc_chunks)

    # Run extraction process
    log.info("Running entity extraction")
    entities = {
        "Contract duration": run_chat_model_entity_extraction(
            entity_name="Contract duration",
            vector_store=vector_store,
            prompt=get_duration_prompt(),
            chat_config=model_config["chat_model"],
            output_parser=months_parser,
            search_k=4,
        ),
        "Buyer termination period by convenience": run_chat_model_entity_extraction(
            entity_name="Buyer termination period by convenience",
            vector_store=vector_store,
            prompt=get_convenience_prompt(contract_type="Buyer"),
            chat_config=model_config["chat_model"],
            output_parser=days_parser,
            search_k=5,
        ),
        "Supplier termination period by convenience": run_chat_model_entity_extraction(
            entity_name="Supplier termination period by convenience",
            vector_store=vector_store,
            prompt=get_convenience_prompt(contract_type="Supplier"),
            chat_config=model_config["chat_model"],
            output_parser=days_parser,
            search_k=5,
        ),
        "Payment terms": run_chain_entity_extraction(
            entity_name="Payment terms",
            vector_store=vector_store,
            chain_config=model_config["terms_chain"],
            output_parser=days_parser,
        ),
        "Buyer termination period by cause": run_chain_entity_extraction(
            entity_name="Buyer termination period by cause",
            vector_store=vector_store,
            chain_config=model_config["cause_chain"],
            output_parser=days_parser,
        ),
    }

    # Write output to db
    log.info("Entity extraction results: %s", entities)

    log.info("Entities extracted, time consumed: %s", round(time.time() - t_ee_start, 2))
    log.info("COMPLETED: Entity Extraction")

    return entities
