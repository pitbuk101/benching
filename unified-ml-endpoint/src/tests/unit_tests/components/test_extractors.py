from unittest.mock import Mock, patch

import pytest
# from azure.ai.formrecognizer import AnalyzeResult, DocumentLine, DocumentPage

# from ada.components.extractors.text_extractors import azure_ocr, split_text_into_pages


@pytest.fixture
def mock_azure_response():
    """Fixture to create a mock Azure OCR response."""
    mock_page = DocumentPage(
        page_number=1,
        lines=[DocumentLine(content="Line 1"), DocumentLine(content="Line 2")],
    )
    return AnalyzeResult(pages=[mock_page])


@patch("ada.components.extractors.text_extractors.DocumentAnalysisClient")
@pytest.mark.components
def test_azure_ocr(mock_client):
    """Test the azure_ocr function with a mocked DocumentAnalysisClient."""
    # Set up the mock client and its return value
    mock_poller = Mock()
    mock_poller.result.return_value = "Mocked AnalyzeResult"
    mock_client.return_value.begin_analyze_document.return_value = mock_poller

    # Call the function with mock parameters
    with open("data/local_contracts/raw/3_gbm_bearings.pdf", "rb") as f:
        result = azure_ocr(f, "dummy_endpoint", "dummy_key", "model")

    mock_client.return_value.begin_analyze_document.assert_called_once()
    assert result == "Mocked AnalyzeResult"


@pytest.mark.components
def test_split_text_into_pages(mock_azure_response):
    """Test the split_text_into_pages function."""
    # Call the function with a mocked response
    result = split_text_into_pages(mock_azure_response)

    # Assert that the text is split correctly into pages
    assert isinstance(result, dict)
    assert result[1] == "Line 1\nLine 2\n"
