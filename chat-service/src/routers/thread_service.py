from src.utils.logs import get_custom_logger
from src.datamodels.request_model import ThreadBaseModel
from src.celery_tasks.tasks import thread_postgress
from celery.result import AsyncResult
from fastapi import APIRouter

logger = get_custom_logger(__name__)

thread_router = APIRouter()

@thread_router.post("/ada/threads/{task}")
async def threads(request: ThreadBaseModel, task: str):
    input_arguments = {
        "tenant_id": request.tenant_id,
        "category": request.category,
        "thread_id": request.thread_id,
        "chat": request.chat,
        "task": task
    }
    task = thread_postgress.delay(**input_arguments)
    logger.info(f"Task: {task}")
    return {"task_id": task.id}

@thread_router.get("/ada/thread-api-status/{task_id}")
async def get_api_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "pending"}
    elif task_result.state == "STARTED":
        return {"status": "started"}
    elif task_result.state == "FAILURE":
        return {"status": "failure", "error": str(task_result.result)}
    elif task_result.state == "SUCCESS":
        if task_result.result:
            return {"status": task_result.status, "result": task_result.result}
        else:
            return {"status": task_result.status}
    
    else:
        return {"status": task_result.state}