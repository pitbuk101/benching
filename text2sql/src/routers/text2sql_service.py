from src.utils.logs import get_custom_logger
from src.datamodels.request_model import QueryRequest
from src.celery_tasks.tasks import text2sql_pipeline
from celery.result import AsyncResult
from fastapi import APIRouter, Request

logger = get_custom_logger(__name__)

text2sql_router = APIRouter()

@text2sql_router.post("/text2sql")
async def ask(request: QueryRequest, orginal_request: Request):
    logger.info(f"Received request: {request}")
    arguments = {**request.model_dump()}
    logger.info(f"Arguments for pipeline execution: {arguments}")
    task = text2sql_pipeline.delay(**arguments)
    return {"task_id": task.id}

@text2sql_router.get("/text2sql/{task_id}")
async def get_ask_details(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "pending"}
    elif task_result.state == "STARTED":
        return {"status": "started"}
    elif task_result.state == "FAILURE":
        return {"status": "failure", "error": str(task_result.result)}
    elif task_result.state == "SUCCESS":
        return {"status": task_result.status, "result": task_result.result.get("result", {})}
    else:
        return {"status": task_result.state}