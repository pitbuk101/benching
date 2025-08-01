from src.utils.logs import get_custom_logger
from src.datamodels.request_model import (
    ChartRecommendationRequest,
    QueryRequest,
    RecommendationRequest
)
from src.celery_tasks.tasks import (
    pipeline_execution,
    recommendation_pipeline,
    chart_recommendation_pipeline
)
from celery.result import AsyncResult
from fastapi import APIRouter, Request

logger = get_custom_logger(__name__)

chat_router = APIRouter()


@chat_router.post("/ada")
async def ask_agent(request: QueryRequest, orginal_request: Request):
    logger.info(f"Received request: {request}")
    arguments = {**request.model_dump(), "auth_token": orginal_request.headers.get("authorization")}
    task = pipeline_execution.delay(**arguments)
    logger.info(f"task: {task}")
    return {"task_id": task.id}

@chat_router.get("/ada/{task_id}")
async def get_response(task_id: str):
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

@chat_router.post("/recommendation")
async def get_recommendation(request: RecommendationRequest):
    logger.info(f"Received request: {request}")
    arguments = {**request.model_dump()}
    logger.info(f"Arguments for recommendation pipeline execution: {arguments}")
    task = recommendation_pipeline.delay(**arguments)
    return {"task_id": task.id}


@chat_router.get("/recommendation/{task_id}")
async def get_response(task_id: str):
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

@chat_router.post("/chart-recommendation")
async def get_recommendation(request: ChartRecommendationRequest):
    logger.info(f"Received request: {request}")
    arguments = {**request.model_dump()}
    logger.info(f"Arguments for recommendation pipeline execution: {arguments}")
    task = chart_recommendation_pipeline.delay(**arguments)
    return {"task_id": task.id}

@chat_router.get("/chart-recommendation/{task_id}")
async def get_response(task_id: str):
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
