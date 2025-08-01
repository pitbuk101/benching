from src.celery_tasks.celery_app import celery_app
from src.utils.logs import get_custom_logger
from src.pipelines.docs_ai.updation_pipeline import update_leakage_in_json

logger = get_custom_logger(__name__)


@celery_app.task(bind=True)
def update_leakage(self, **kwargs):
    conn_params = kwargs.get("conn_params", {})
    database = kwargs.get("database", None)
    schema = kwargs.get("schema", None)
    upload_id = kwargs.get("upload_id", None)
    tenant_id = kwargs.get("tenant_id", None)
    category = kwargs.get("category", None)
    sql_template_path = kwargs.get("sql_template_path", None)
    try:
        status = update_leakage_in_json(conn_params, database, schema, upload_id, tenant_id, category, sql_template_path)
        logger.info(f"Leakage update_leakage status: {status}")
        return status
    except Exception as e:
        logger.exception(f"Error in update_leakage: {e}")
        return {"error": str(e)}
    
