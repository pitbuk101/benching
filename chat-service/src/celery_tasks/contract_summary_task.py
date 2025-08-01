from src.celery_tasks.celery_app import celery_app
from src.utils.logs import get_custom_logger
from src.pipelines.docs_ai.update_contract_summary import update_contract_summary, update_extracted_invoice

logger = get_custom_logger(__name__)


@celery_app.task(bind=True)
def update_snowflake_contracts(self, **kwargs):
    conn_params = kwargs.get("conn_params", {})
    database = kwargs.get("database", None)
    upload_id = kwargs.get("upload_id", None)
    entity_json = kwargs.get("entity_json", {})
    tenant_id = kwargs.get("tenant_id", None)
    schema = kwargs.get("schema", None)
    sql_template_path = kwargs.get("sql_template_path", None)
    try:
        status = update_contract_summary(conn_params, database, schema, upload_id, entity_json, tenant_id, sql_template_path)
        logger.info(f"Snowflake contracts update status: {status}")
        return status
    except Exception as e:
        logger.exception(f"Error in update_snowflake_contracts: {e}")
        return {"error": str(e)}
    
@celery_app.task(bind=True)
def update_snowflake_invoice(self, **kwargs):
    conn_params = kwargs.get("conn_params", {})
    database = kwargs.get("database", None)
    schema = kwargs.get("schema", None)
    upload_id = kwargs.get("upload_id", None)
    entity_json = kwargs.get("entity_json", {})
    tenant_id = kwargs.get("tenant_id", None)
    sql_template_path = kwargs.get("sql_template_path", None)
    try:
        status = update_extracted_invoice(conn_params, database, schema, upload_id, entity_json, tenant_id, sql_template_path)
        logger.info(f"Snowflake Invoice update status: {status}")
        return status
    except Exception as e:
        logger.exception(f"Error in update_snowflake_invoice: {e}")
        return {"error": str(e)}