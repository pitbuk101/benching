#!/usr/bin/env python

import base64
import os
import uuid
from pathlib import Path

import fitz
from fitz import Page

from ada.components.llm_models.generic_calls import generate_chat_response
from ada.utils.config.config_loader import read_config

conf = read_config("azml_deployment.yaml")


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure directory exists, if not create it.
    args:
        directory_path: str: Path to directory
    return:
        None
    """
    path = Path(directory_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")


# Convert pages from PDF to images
def extract_pdf_pages_to_images_or_text(pdf_path: str, image_dir: str, markdown_dir: str) -> str:
    """
    Extract pdf pages and for each of them, decide if OCR is needed.
     If yes then take screenshot and save it in image_out directory.
    If OCR is not needed then extract text from the page and save it in markdown_out directory.
    args:
        pdf_path: str: Path to input PDF file
        image_dir: str: Path to directory where screenshot images will be saved. This will be deleted after processing.
        markdown_dir: str: Path to directory where extracted text will be saved. This will be deleted after processing.
    return:
        doc_id: str: Unique identifier for the document
    """
    # Validate image_out directory exists
    doc_id = str(uuid.uuid4())
    image_out_dir = os.path.join(image_dir, doc_id)
    ensure_directory_exists(image_out_dir)
    markdown_out_dir = os.path.join(markdown_dir, doc_id)
    ensure_directory_exists(markdown_out_dir)

    # Open the PDF file and iterate pages
    print("Extracting images from PDF...")
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        image_page_ratio = get_image_area_percentage(page)
        table_cnt = len(page.find_tables().tables)
        ocr_image_to_page_percentage_threshold = float(
            conf["components"]["doc2md"]["ocr_image_to_page_percentage_threshold"],
        )
        if image_page_ratio < ocr_image_to_page_percentage_threshold and table_cnt == 0:
            print(f"Page {page_number + 1} does not contain any images or tables.")
            text = page.get_text()
            markdown_file_out = os.path.join(markdown_out_dir, f"{page_number + 1}.txt")
            with open(markdown_file_out, "w", encoding="utf-8") as md_out:
                md_out.write(text)
        else:
            print(f"Page {page_number + 1} contains images or tables. Taking screenshot")
            image = page.get_pixmap()
            image_out_file = os.path.join(image_out_dir, f"{page_number + 1}.png")
            image.save(image_out_file)

    return doc_id


# Base64 encode images
def encode_image(image_path: str) -> str:
    """
    Read the image and encode using base64 and decode using utf-8
    args:
        image_path: str: Path to image file
    return:
        str: Encoded image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_all_files(directory_path: str) -> list[str]:
    """
    Get all files in the directory
    args:
        directory_path: str: Path to directory
    return:
        list: List of files in the directory
    """
    files = []
    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)
        if os.path.isfile(entry_path):
            files.append(entry_path)
    return files


def extract_markdown_from_image_using_vlm(image_path: str):
    """
    Extract the markdown from image using VLM. The image is encoded and sent to VLM for processing.
    args:
        image_path: str: Path to image file
    return:
        str: Extracted markdown
    """
    try:
        base64_image = encode_image(image_path)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Extract everything you see in this image to markdown.
                        Convert all charts such as line, pie and bar charts to markdown tables.
                         Do not embed images in the markdown.
                    """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            },
        ]

        md_text = generate_chat_response(messages, model="gpt-4o")
        return md_text
    except Exception:
        return ""


def process_image(file: str, markdown_out_dir: str) -> str:
    """
    Process the image to extract markdown using VLM.
    args:
        file: str: Path to image file
        markdown_out_dir: str: Path to directory where markdown for each image will be saved
    return:
        str: Path to image file
    """
    if ".png" in file:
        print("Processing:", file)
        markdown_file_out = os.path.join(
            markdown_out_dir,
            os.path.basename(file).replace(".png", ".txt"),
        )
        print(markdown_file_out)
        if not os.path.exists(markdown_file_out):
            markdown_text = extract_markdown_from_image_using_vlm(file)
            with open(markdown_file_out, "w", encoding="utf-8") as md_out:
                md_out.write(markdown_text)
        else:
            print("Skipping processed file.")
    else:
        print("Skipping non PNG file:", file)

    return file


def get_image_area_percentage(page: Page) -> float:
    """
    Get the percentage of image area in the page. This is used to decide if OCR is needed.
    args:
        page: fitz.Page: Page object from PyMuPDF
    return:
        float: Percentage of image area in the page
    """
    d = page.get_text("dict")
    blocks = d["blocks"]  # the list of block dictionaries
    imgblocks = [b for b in blocks if b["type"] == 1]
    page_area = abs(page.rect)
    image_area = 0
    for img in imgblocks:
        image_area += abs(fitz.Rect(img["bbox"]) & page.rect)
    return round(image_area * 100 / page_area, 2)
