import base64
import unittest
from unittest.mock import MagicMock, mock_open, patch

import fitz

from ada.components.extractors.doc_to_markdown import doc2md_utils


@patch("ada.components.extractors.doc_to_markdown.doc2md_utils.Path.mkdir")
@patch("ada.components.extractors.doc_to_markdown.doc2md_utils.Path.exists", return_value=False)
def test_ensure_directory_exists(mock_exists, mock_mkdir):
    doc2md_utils.ensure_directory_exists("some/directory/path")
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


@patch("ada.components.extractors.doc_to_markdown.doc2md_utils.Path.exists", return_value=True)
def test_ensure_directory_exists_already_exists(mock_exists):
    doc2md_utils.ensure_directory_exists("some/directory/path")
    mock_exists.assert_called_once()


@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.conf",
    return_value={"components": {"doc2md": {"ocr_image_to_page_percentage_threshold": 5}}},
)
@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.get_image_area_percentage",
    return_value=0,
)
@patch("ada.components.extractors.doc_to_markdown.doc2md_utils.ensure_directory_exists")
@patch("fitz.open")
def test_extract_pdf_pages_to_images_or_text(
    mock_fitz_open,
    mock_ensure_directory_exists,
    mock_get_image_area_percentage,
    mock_conf,
):
    mock_page = MagicMock()
    mock_page.get_text.return_value = "some text"
    mock_fitz_open.return_value = mock_page

    doc_id = doc2md_utils.extract_pdf_pages_to_images_or_text(
        "some/pdf/path",
        "some/image/dir",
        "some/markdown/dir",
    )
    assert doc_id is not None
    mock_ensure_directory_exists.assert_called()


@patch("builtins.open", new_callable=mock_open, read_data=b"image data")
def test_encode_image(mock_file):
    encoded_image = doc2md_utils.encode_image("some/image/path")
    assert encoded_image == base64.b64encode(b"image data").decode("utf-8")


@patch("os.listdir", return_value=["file1.txt", "file2.txt"])
@patch("os.path.isfile", return_value=True)
def test_get_all_files(mock_isfile, mock_listdir):
    files = doc2md_utils.get_all_files("some/directory/path")
    assert files == ["some/directory/path/file1.txt", "some/directory/path/file2.txt"]


@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.generate_chat_response",
    return_value="markdown text",
)
@patch("builtins.open", new_callable=mock_open, read_data=b"image data")
def test_extract_markdown_from_image_using_vlm(mock_file, mock_generate_chat_response):
    markdown_text = doc2md_utils.extract_markdown_from_image_using_vlm("some/image/path")
    assert markdown_text == "markdown text"


@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.extract_markdown_from_image_using_vlm",
    return_value="markdown text",
)
@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists", return_value=False)
def test_process_image(mock_exists, mock_file, mock_extract_markdown):
    result = doc2md_utils.process_image("some/image/path.png", "some/markdown/dir")
    assert result == "some/image/path.png"
    mock_extract_markdown.assert_called_once()


@patch("fitz.Page.get_text", return_value={"blocks": [{"type": 1, "bbox": [0, 0, 1, 1]}]})
def test_get_image_area_percentage(mock_get_text):
    mock_page = MagicMock()
    mock_page.get_text.return_value = {"blocks": [{"type": 1, "bbox": [0, 0, 1, 1]}]}
    mock_page.rect = fitz.Rect(0, 0, 2, 2)

    percentage = doc2md_utils.get_image_area_percentage(mock_page)
    assert percentage == 25.0


if __name__ == "__main__":
    unittest.main()
