"""Defines all the calls to be used in benchmarking."""

from typing import Collection

from langchain_core.documents import Document

from ada.utils.logs.logger import get_logger

log = get_logger("benchmarking_calls.py")


def process_data_extractor_response(
    response: tuple[str, list[Document]],
) -> dict[str, str | Collection[str]]:
    """
    Function add sources from document for each response.
    Args:
        response (tuple[str, list[Document]]): LLM model response
    Returns:
        dict[str, str| Collection[str]]: Sources from document for each response
    """
    processed_response = {"answer": response[0], "source": {}}
    for document in response[1]:
        doc_metadata = document.metadata
        source = doc_metadata["source"]
        page_content = document.page_content
        processed_response["source"][source] = page_content  # type: ignore
    return processed_response
