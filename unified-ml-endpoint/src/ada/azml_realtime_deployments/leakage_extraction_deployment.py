"""Azure ML Endpoint for Leakage extraction deployment."""
import json
import pathlib
import sys
from typing import Any

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.components.db.pg_connector import PGConnector
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("leakage_extraction")


def init():
    """Azure Realtime deployment for leakage extraction"""


def run(inputs: str) -> dict[str, list[dict[str, Any]]]:
    """
    Entrypoint function for Leakage Extraction
    Args:
        inputs: payload

    Returns: extracted leakage from Database

    """
    inputs = json.loads(inputs)

    pg_db_conn = PGConnector(inputs["tenant_id"], cursor_type="real_dict")
    data = pg_db_conn.select_records_with_filter(
        table_name="contract_sku_details",
        filtered_columns=read_config("use-cases.yml")["leakage"][
            "contract_sku_details_table_columns"
        ],
        filter_condition=f"document_id = {inputs['document_id']}",
    )
    pg_db_conn.close_connection()
    log.info(
        "Extracted leakage data for document id %s is below: \n %s", inputs["document_id"], data
    )
    return {"contract_sku_details": [dict(row) for row in data]}
