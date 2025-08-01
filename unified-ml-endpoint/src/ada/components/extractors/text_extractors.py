"""Text Extractor"""
from typing import IO, Dict

import numpy as np
import pandas as pd
# from azure.ai.formrecognizer import AnalyzeResult, DocumentAnalysisClient
# from azure.core.credentials import AzureKeyCredential

from ada.utils.format.format import check_empty_or_non_word_text
from ada.utils.logs.logger import get_logger

log = get_logger("text_extractors")


def azure_ocr(
    contract_path: IO[bytes],
    vision_endpoint: str,
    vision_key: str,
    model: str = "prebuilt-document",
) -> AnalyzeResult:
    """
    Send uploaded file to azure ocr.

    Args:
        contract_path: Upload file object.
        vision_endpoint: The AzureML Vision endpoint for the environment
        vision_key: The API Key for the AzureML Vision service
        model: the type of model to use for OCR

    Returns:
        Text after Azure OCR read
    """
    document_analysis_client = DocumentAnalysisClient(
        endpoint=vision_endpoint, credential=AzureKeyCredential(vision_key)
    )
    document = contract_path.read()
    poller = document_analysis_client.begin_analyze_document(
        model, document=document, locale="en-US"
    )
    result = poller.result()

    return result


def split_text_into_pages(azure_ocr_output: AnalyzeResult) -> Dict:
    """Take json from azure ocr and split based on pages."""
    extracted_text = {}

    for page in azure_ocr_output.pages:
        log.info("----Analyzing document from page # %s----", page.page_number)
        page_content = ""
        if len(page.lines) != 0:
            for line in page.lines:
                page_content += line.content + "\n"
            if not check_empty_or_non_word_text(page_content):
                extracted_text[page.page_number] = page_content

    return extracted_text


def extract_tables_from_ocr_output(
    azure_ocr_output: AnalyzeResult,
) -> list[tuple[int, pd.DataFrame]]:
    """
    This function accepts the output from Azure OCR as input.
    It extracts all the data from the tables and creates a dataframe for each one.

    Args:
        azure_ocr_output: Text after Azure OCR read

    Returns:
        A list of tuple with page number and pandas dataframe
    """
    log.info("Extracting Tables from ocr output")
    extracted_tables = []
    for table in azure_ocr_output.tables:
        page_number = None
        rows, columns = table.row_count, table.column_count
        table_rows = [[np.NaN] * columns for _ in range(rows)]
        for cell in table.cells:
            if page_number is None:
                page_number = cell.bounding_regions[0].page_number

            for row_num in range(cell.row_span):
                for col_num in range(cell.column_span):
                    table_rows[cell.row_index + row_num][cell.column_index + col_num] = cell.content
        extracted_tables.append((page_number, pd.DataFrame.from_records(table_rows)))

    return extracted_tables
