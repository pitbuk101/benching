from asgiref.sync import async_to_sync
from src.celery_tasks.celery_app import celery_app
from src.utils.logs import get_custom_logger
from src.providers.database.postgres_driver import PostgresDatabaseFactory
from src.env import (
    PGUSER,
    PGPASSWORD,
    PGHOST,
    PGPORT,
    PGDATABASE
)

logger = get_custom_logger(__name__)


@celery_app.task(bind=True)
def update_pg_status(self, **kwargs):
    table = kwargs.get("table", None)
    upload_id = kwargs.get("upload_id", None)
    status = kwargs.get("status", None)
    schema = kwargs.get("schema", None)

    pg_conn_params = {
        "user": PGUSER,
        "password": PGPASSWORD,
        "host": PGHOST,
        "port": PGPORT,
        "database": PGDATABASE
    }

    try:
        pg_conn = PostgresDatabaseFactory(pg_conn_params)
        async_to_sync(pg_conn.update_status)(table, upload_id, status, schema)
        logger.info(f"Updated {table} with {upload_id}={status} in schema={schema}")
        logger.info(f"Leakage update_leakage status: {status}")

    except Exception as e:
        logger.exception(f"Error in update_leakage: {e}")
        return {"error": str(e)}