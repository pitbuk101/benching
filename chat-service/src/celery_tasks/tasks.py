import json
from src.celery_tasks.celery_app import celery_app
from src.utils.logs import get_custom_logger
from src.pipelines.orchestrator import (
    flow,
    question_recommendation_flow,
    chart_recommendation_flow,
    orchestrate_snowflake_entities,
    orchestrate_thread_pipeline
)
logger = get_custom_logger(__name__)

@celery_app.task(bind=True)
def pipeline_execution(self, **kwargs):
    logger.info(f"[Celery Task Start] Task ID: {self.request.id}")
    try:
        input_arguments = {
            "tenant_id": kwargs.get("tenant_id"),
            "user_input": f"{kwargs.get('query')}",
            "session_id": kwargs.get("session_id"),
            "thread_id": kwargs.get("thread_id"),
            "preferred_currency": kwargs.get("preferred_currency"),
            "category": kwargs.get("category"),
            "language": kwargs.get("language"),
            "auth_token": kwargs.get("auth_token"),
            "region": kwargs.get("region")
        }
        result = flow.invoke(input_arguments)
        return {"status": "completed", "result": result['final_response']}
    except Exception as e:
        logger.exception(f"Error in pipeline execution: {e}")
        self.retry(exc=e, max_retries=0)

@celery_app.task(bind=True)
def recommendation_pipeline(self, **kwargs):
    logger.info(f"[Celery Task Start] Task ID: {self.request.id}")
    try:
        input_arguments = {
            "previous_questions": kwargs.get('previous_questions', []),
            "tenant_id": kwargs.get("tenant_id"),
            "session_id": kwargs.get("session_id"),
            "preferred_currency": kwargs.get("preferred_currency"),
            "category": kwargs.get("category"),
            "language": kwargs.get("language"),
            "region": kwargs.get("region")
        }
        logger.info(f"Executing recommendation pipeline with arguments: {input_arguments}")
        # result = asyncio.run(question_recommendation_flow.ainvoke({**input_arguments}))
        # ✅ Safe async call from sync code
        result = question_recommendation_flow.invoke(input_arguments)
        # result = await question_recommendation_flow.ainvoke(input_arguments)
        return {"status": "completed", "result": result['recommendations']}
    except Exception as e:
        logger.exception(f"Error in recommendation pipeline: {e}")
        self.retry(exc=e, countdown=1, max_retries=0)


@celery_app.task(bind=True)
def chart_recommendation_pipeline(self, **kwargs):
    logger.info(f"[Celery Task Start] Task ID: {self.request.id}")
    try:
        input_arguments = {
            "user_question": kwargs.get('user_question', []),
            "tenant_id": kwargs.get("tenant_id"),
            "preferred_currency": kwargs.get("preferred_currency"),
            "preferred_language": kwargs.get("language"),
            "category": kwargs.get("category"),
            "data": kwargs.get("data"),
            "columns": kwargs.get("columns")
        }
        logger.info(f"Executing recommendation pipeline with arguments: {input_arguments}")
        result = chart_recommendation_flow.invoke(input_arguments)
        return {"status": "completed", "result": result['charts']}
    except Exception as e:
        logger.exception(f"Error in recommendation pipeline: {e}")
        self.retry(exc=e, countdown=1, max_retries=0)

@celery_app.task(bind=True)
def process_snowflake_entities_task(self, **kwargs):
    logger.info(f"[Celery Task Start] Task ID: {self.request.id}")
    tenant_id = kwargs.get("tenant_id")
    upload_ids = kwargs.get("upload_ids", [])
    try:
        updated_rows = orchestrate_snowflake_entities(tenant_id, upload_ids)
        return {"updated_rows": updated_rows}
    except Exception as e:
        logger.exception(f"Error in process_snowflake_entities_task: {e}")
        return {"error": str(e)}

@celery_app.task(bind=True)
def thread_postgress(self, **kwargs):
    logger.info(f"[Celery Task Start] Task ID: {self.request.id}")
    input_args = {
        "tenant_id": kwargs.get("tenant_id"),
        "category": kwargs.get("category"),
        "thread_id": kwargs.get("thread_id"),
    }
    thread = orchestrate_thread_pipeline(**input_args)
    task = (kwargs.get("task") or "").lower()
    status = None
    try:
        task_map = {
            "save": lambda: thread.save_thread(chat=json.dumps(kwargs.get("chat", ""))),
            "list": thread.list_thread,
            "update": lambda: thread.update_thread(chat=json.dumps(kwargs.get("chat", ""))),
            "delete": thread.delete_thread,
            "get": thread.get_thread,
        }
        if task in task_map:
            status = task_map[task]()
        else:
            logger.warning(f"Unknown task: {task}")
    except Exception as e:
        logger.exception(f"Error occurred in thread_postgress for task '{task}': {e}")
    return status