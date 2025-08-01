from src.celery_tasks.celery_app import celery_app
from src.utils.logs import get_custom_logger
from src.pipelines.orchestrator import flow

logger = get_custom_logger(__name__)

@celery_app.task(bind=True)
def text2sql_pipeline(self, **kwargs):
    try:
        input_arguments = {
            "user_query": kwargs.get("user_query"),
            "tenant_id": kwargs.get("tenant_id"),
            "category": kwargs.get("category")
        }
        logger.info(f"Executing pipeline with arguments: {input_arguments}")
        result = flow.invoke(input_arguments)
        logger.debug(f"Result: {result}")
        return {
            "status": "completed", 
            "result": {
                "sql":result['final_sql'],
                "fixed_query": result['fixed_query'],
                "cache": result["cache"]
            }
            
        }
    except Exception as e:
        logger.exception(f"Error in Text2SQL Pipeline Execution: {e}")
        self.retry(exc=e, max_retries=0)