import os
import unittest
from unittest.mock import mock_open, patch

from ada.components.extractors.doc_to_markdown import doc2md


@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.extract_pdf_pages_to_images_or_text",
    return_value="doc_id",
)
@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.get_all_files",
    return_value=["image1.png", "image2.png"],
)
@patch(
    "ada.components.extractors.doc_to_markdown.doc2md_utils.process_image",
    side_effect=["image1.png", "image2.png"],
)
@patch("concurrent.futures.ThreadPoolExecutor")
@patch("shutil.rmtree")
@patch("builtins.open", new_callable=mock_open, read_data="extracted text")
@patch("glob.glob", return_value=["markdown_dir/doc_id/1.txt", "markdown_dir/doc_id/2.txt"])
@patch(
    "ada.components.extractors.doc_to_markdown.doc2md.conf",
    return_value={"components": {"doc2md": {"max_workers": 2}}},
)
def test_extract_text_from_pdf(
    mock_conf,
    mock_glob,
    mock_open,
    mock_rmtree,
    mock_executor,
    mock_process_image,
    mock_get_all_files,
    mock_extract_pdf,
):
    pdf_path = "some/pdf/path"
    image_path = "some/image/path"
    markdown_path = "some/markdown/path"

    mock_executor.return_value.__enter__.return_value.map.return_value = [
        "image1.png",
        "image2.png",
    ]

    combined_text = doc2md.extract_text_from_pdf(pdf_path, image_path, markdown_path)

    assert combined_text == "\nextracted text\nextracted text"
    mock_extract_pdf.assert_called_once_with(pdf_path, image_path, markdown_path)
    mock_get_all_files.assert_called_once_with(os.path.join(image_path, "doc_id"))
    mock_rmtree.assert_any_call(os.path.join(image_path, "doc_id"))
    mock_rmtree.assert_any_call(os.path.join(markdown_path, "doc_id"))


if __name__ == "__main__":
    unittest.main()
