"""Leakage use case."""

from ada.components.db.pg_connector import PGConnector
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("leakage_data_retriever")


def retrieve_leakage_data(tenant_id, document_id):
    """
    Retrieves leakage data from the database for a given tenant and document.

    Args:
        tenant_id (str): The unique identifier for the tenant.
        document_id (int): The unique identifier for the document.

    Returns:
        dict: A dictionary containing the leakage data for the specified document,
              structured as:
              {
                  "contract_sku_details": [
                      {<column_name>: <value>, ...},
                      ...
                  ]
              }
    """
    pg_db_conn = PGConnector(tenant_id, cursor_type="real_dict")
    data = pg_db_conn.select_records_with_filter(
        table_name="contract_sku_details",
        filtered_columns=read_config("use-cases.yml")["leakage"][
            "contract_sku_details_table_columns"
        ],
        filter_condition=f"document_id = {document_id}",
    )
    pg_db_conn.close_connection()
    log.info(
        "Extracted leakage data for document id %s is below: \n %s",
        document_id,
        data,
    )
    return {"contract_sku_details": [dict(row) for row in data]}
