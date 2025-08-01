import concurrent.futures
import glob
import os
import shutil
from functools import partial

import ada.components.extractors.doc_to_markdown.doc2md_utils as doc2md_utils
from ada.utils.config.config_loader import read_config

conf = read_config("azml_deployment.yaml")


def extract_text_from_pdf(pdf_path: str, image_path: str, markdown_path: str) -> str:
    """
    Extract text from PDF file. This function will extract images from PDF file and then process them to extract text.
    This function will internally decide if OCR is needed for the image or not.
     Charts and tables are converted to markdown tables.
    args:
        pdf_path: str: Path to input PDF file
        image_path: str: Path to directory where screenshot images will be saved. These files will be deleted after processing.
        markdown_path: str: Path to directory where extracted text will be saved. These files will be deleted after processing.
    return:
        combined_text: str: Extracted text from the PDF. It will have some markdown formatting.
    """
    doc_id = doc2md_utils.extract_pdf_pages_to_images_or_text(pdf_path, image_path, markdown_path)

    pdf_images_dir = os.path.join(image_path, doc_id)

    files = doc2md_utils.get_all_files(pdf_images_dir)

    markdown_out_dir = os.path.join(markdown_path, doc_id)
    partial_process_image = partial(doc2md_utils.process_image, markdown_out_dir=markdown_out_dir)
    max_workers = int(conf["components"]["doc2md"]["max_ocr_workers"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the partial function to the array of items
        results = list(executor.map(partial_process_image, files))

    print("Total Processed:", len(results))

    combined_text = ""
    for file_path in sorted(
        glob.glob(markdown_out_dir + "/*.txt"),
        key=lambda x: int(x.split("/")[-1].split(".")[0]),
    ):
        with open(file_path) as file:
            combined_text = combined_text + "\n" + file.read()
    shutil.rmtree(pdf_images_dir)
    shutil.rmtree(markdown_out_dir)
    return combined_text


if __name__ == "__main__":
    image_path = "../../../../../downloads/OCR/images"
    markdown_path = "../../../../../downloads/OCR/markdown"
    pdf_path = "/Users/Prathamesh_Kalamkar/git_repos/orp-genai/downloads/OCR/2024 Ocean Strategy Review (003) (002).pdf"

    extracted_text = extract_text_from_pdf(pdf_path, image_path, markdown_path)
    output_txt_path = "../../../../../downloads/OCR/" + os.path.basename(pdf_path).replace(
        ".pdf",
        ".txt",
    )
    with open(output_txt_path, "w") as f:
        f.write(extracted_text)
