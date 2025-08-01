"""Preprocessing wrapper to run batch pipeline components locally."""

import json
import os
import pathlib
from argparse import Namespace

from ada.azml_components.preprocessing import call_nodes, db_write
from ada.components.db.pg_connector import PGConnector
# from ada.components.extractors.text_extractors import azure_ocr
from ada.use_cases.pdf_reader.pdf_reader import run_pdf_reader
from ada.utils.azml.azml_utils import set_openai_api_creds
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("local_preprocessing_pipeline")

conf = read_config("preprocessing-params.yml")
component_conf = read_config("models.yml")

set_openai_api_creds(
    {
        "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    },
)


def get_ocr_output(filename: str):
    """Get OCR output."""
    repo_root = pathlib.Path(__file__).parents[2]
    filepath = os.path.join(repo_root, "data", "local_contracts", "raw", filename)
    with open(filepath, "rb") as raw_contract:
        return azure_ocr(
            contract_path=raw_contract,
            vision_endpoint=component_conf["vision_endpoint"],
            vision_key=os.getenv("VISION_KEY"),
        )


if __name__ == "__main__":
    set_openai_api_creds(
        {
            "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        },
    )

    nodes_mapping = {
        "pdf-reader": run_pdf_reader,
        "call-nodes": call_nodes,
        "db-writer": db_write,
    }

    for run_config in conf["local-runs"]:
        payload = run_config["example-payload"]
        payload["sku_list"] = json.dumps(payload["sku_list"])
        nodes = run_config["pipeline-nodes"]
        if "pdf-reader" in nodes:
            scanned_pdf = get_ocr_output(payload.get("input_data_filename"))
            # Converting payload dict to Namespace object to mimic args from argparse.
            doc_chunks, doc_info, doc_tables = run_pdf_reader(
                document_id=payload.get("document_id"),
                input_data_filename=payload.get("input_data_filename"),
                document_type=payload.get("document_type"),
                category=payload.get("category"),
                azure_ocr_output=scanned_pdf,
                embedding_model=payload.get("embedding_model"),
            )
            nodes.remove("pdf-reader")
            log.info("ran pdf reader")
            params = {
                "args": Namespace(**payload),
                "df_doc_chunks": doc_chunks,
                "df_doc_info": doc_info,
                "df_doc_tables": doc_tables,
            }
            output_dfs = nodes_mapping["call-nodes"](**params)  # type: ignore
            nodes_mapping["db-writer"](  # type: ignore
                output_dfs,
                PGConnector(tenant_id=payload.get("tenant_id")),
                args=Namespace(**payload),
            )
            log.info("preprocessing pipeline ran successfully")
