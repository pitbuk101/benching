from src.utils.logs import get_custom_logger
from src.celery_tasks.celery_app import celery_app
from src.providers.cache_store.redis_cache import cache
logger = get_custom_logger(__name__)



@celery_app.task(bind=True)
def create_cache(self, **kwargs):
    key = kwargs["key"]
    value = kwargs["value"]
    logger.info(f"Ingesting Redis Cache for key: {key}")
    # Storing the cache for 7 days
    cache_time = 60 * 60 * 24 * 7
    cache.ingest(data={key: value}, ex=cache_time)
