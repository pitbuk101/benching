"""
Summary generator component for batch pipeline
"""

from typing import Any

import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from ada.components.llm_models.chunks import create_chunks
from ada.components.llm_models.generic_calls import generate_embeddings_from_string
from ada.components.llm_models.model_base import Model
from ada.use_cases.summary.prompts import (
    CONTRACT_SUMMARY_TEMPLATE,
    DOCUMENT_SUMMARY_TEMPLATE,
    get_reduce_template,
    summary_prompt,
)
from ada.use_cases.summary.summary_util import generate_summary_chain
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.context_manager import (
    UseCase,
    set_tenant_and_intent_flow_context,
)

log = get_logger("summary_generator")
config = read_config("use-cases.yml")["summary"]


# can be moved to llm_models runner
def query_llm_summary(data_chunks: list[Any], document_type: str) -> str:
    """
    Generate LLM summary from data chunk.

    Args:
        data_chunks (list[Any]): list of data chunks
        document_type (str): type of document contract or document
    Returns:
        (str): final summary output
    """
    # hardcoded values for temperature and engine
    llm = Model(name=config["summary_model"], temp=0).obj

    if document_type == "contract":
        template = CONTRACT_SUMMARY_TEMPLATE
    else:
        template = DOCUMENT_SUMMARY_TEMPLATE
    map_prompt = summary_prompt(template)

    log.info("%s summarization in progress...", document_type)

    map_chain = map_prompt | llm | StrOutputParser()

    reduce_prompt = PromptTemplate(
        input_variables=["docs"],
        template=get_reduce_template(document_type),
    )
    reduce_chain = reduce_prompt | llm | StrOutputParser()

    summary_graph = generate_summary_chain(llm, map_chain, reduce_chain)
    output = summary_graph.invoke(
        {"contents": data_chunks},
        {"recursion_limit": 10},
    )
    output = output.get("final_summary", "")
    log.info("%s summarization run in progress...", output)

    if document_type == "contract":
        section_titles = [
            "1. General Purpose:",
            "2. Contract Length & Renewal:",
            "3. Payment Terms:",
            "4. Performance Management:",
            "5. Default:",
            "6. Termination:",
        ]
        for title in section_titles:
            output = output.replace(title, "")

    return output


def generate_summary_and_embeddings(
    document_type: str,
    df_document_chunk: pd.DataFrame,
) -> tuple[str, list[float]]:
    """Generate summary and embeddings
    Args:
        document_type (str): Type of the document `contract` or `document`
        df_document_chunk (pd.DataFrame): the document chunks
    Returns:
        tuple[str, pd.DataFrame]: The final summary and the embeddings
    """

    chunk_contents = df_document_chunk.sort_values(by="chunk_id", ascending=True)[
        "chunk_content"
    ].tolist()

    # split sample text into chunks (temp step)
    data_chunks = []
    for chunk in chunk_contents:
        tmp_data_chunk = create_chunks(chunk)
        for document in tmp_data_chunk:
            data_chunks.append(document)

    # run the chain
    summary = query_llm_summary(data_chunks, document_type)

    log.info("Summary generated from content chunks: \n%s", summary)

    # used replace to handle apostrophe to write data to database.
    # Must be handled by PGConnector in future.
    summary = summary.replace("'", "''").replace("\n\n", "\n")
    summary_embedding = generate_embeddings_from_string(summary)

    log.info("Embeddings successfully generated for summary chunks")

    return summary, summary_embedding


def run_summary_generator(
    document_type: str,
    df_doc_chunks: pd.DataFrame,
    tenant_id: str,
) -> tuple[str, list[float]]:
    """Run summary generator.
    Args:
        document_type (str): The type of the document `contract` or `document`
        df_doc_chunks (pd.DataFrame): DataFrame of the document chunks
    Returns:
        tuple[str, pd.DataFrame]: Final summary and embeddings
    """
    set_tenant_and_intent_flow_context(tenant_id, UseCase.CONTRACT_SUMMARY)
    log.info("Initializing Summary generation")
    document_type = document_type.lower().strip()
    summary, summary_embeddings = generate_summary_and_embeddings(
        document_type,
        df_doc_chunks,
    )
    log.info("COMPLETED: Summary generation")
    return summary, summary_embeddings
