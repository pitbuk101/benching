from ada.components.db.pg_connector import PGConnector
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("news_extraction")
news_insights_conf = read_config("use-cases.yml")["news_insights"]


def retrieve_curated_news_insights_data(tenant_id, date_int):
    """
    Args:
        tenant_id: respective tenant_id
        date_int: Date on which we need to fetch insights for - format YYYYMMDD

    Returns:
        Returns the curated news insights for the given date
    """
    pg_db_conn = PGConnector(tenant_id, cursor_type="real_dict")
    data = pg_db_conn.select_records_with_filter(
        table_name=news_insights_conf["tables"]["news_insights_tbl"],
        filtered_columns=news_insights_conf["columns"]["news_insights_tbl_cols"],
        filter_condition=f"created_at = {date_int}",
    )
    pg_db_conn.close_connection()
    log.info("Extracted curated news insights data is below: \n %s", data)
    return {"curated_news_insights": [dict(row) for row in data]}


def retrieve_news_pipeline_status(tenant_id, date_int):
    """
    Retrieves the status of the news pipeline for a specific tenant and timestamp.

    Args:
        tenant_id (str): The unique identifier for the tenant.
        date_int (str): A time/date equivalent integer in the format "YYYYMMDD")
                             representing the ZIP file or pipeline run time.
    """
    pg_db_conn = PGConnector(tenant_id, cursor_type="real_dict")
    data = pg_db_conn.select_records_with_filter(
        table_name=news_insights_conf["tables"]["news_curation_status_table"],
        filtered_columns=news_insights_conf["columns"]["news_curation_status_columns"],
        filter_condition=f"date_run_int = {date_int}",
    )
    pg_db_conn.close_connection()
    log.info("Extracted curated news insights status  is below: \n %s", data)
    return {"news_pipeline_status": [dict(row) for row in data]}
