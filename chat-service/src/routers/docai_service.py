from src.utils.logs import get_custom_logger
from src.datamodels.request_model import ProcessEntitiesRequest
from src.celery_tasks.tasks import process_snowflake_entities_task
from celery.result import AsyncResult
from fastapi import APIRouter

logger = get_custom_logger(__name__)

docai_router = APIRouter()

@docai_router.post("/docai-entities-extraction")
async def trigger_process_snowflake_entities(request: ProcessEntitiesRequest):
    input_arguments = {
        "tenant_id": request.tenant_id,
        "upload_ids": request.upload_ids
    }
    task = process_snowflake_entities_task.delay(**input_arguments)
    return {"task_id": task.id}

@docai_router.get("/docai-entities-extraction/{task_id}")
async def get_process_snowflake_entities_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "pending"}
    elif task_result.state == "STARTED":
        return {"status": "started"}
    elif task_result.state == "FAILURE":
        return {"status": "failure", "error": str(task_result.result)}
    elif task_result.state == "SUCCESS":
        return {"status": task_result.status, "result": task_result.result}
    else:
        return {"status": task_result.state}