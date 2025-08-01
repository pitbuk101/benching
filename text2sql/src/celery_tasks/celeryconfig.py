import ssl
from src.env import REDIS_HOSTNAME, REDIS_PORT, REDIS_PASSWORD
from src.utils.logs import get_custom_logger

logger = get_custom_logger(__name__)
logger.info("Loading Celery configuration...")

if REDIS_HOSTNAME in {"redis", "localhost"}:
    logger.info("Using local Redis instance")
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}/2"
    broker_use_ssl = None
    result_backend_use_ssl = None
else:
    logger.info("Using AWS ElastiCache Redis instance")
    
    # URL must include ssl_cert_reqs as a query param
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = (
        f"rediss://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}/2"
        "?ssl_cert_reqs=CERT_REQUIRED"
    )

    # SSL options for Redis TLS — provide path to Amazon's CA bundle
    broker_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_REQUIRED,
    }
    result_backend_use_ssl = broker_use_ssl

# Required Celery settings
broker_url = CELERY_BROKER_URL
result_backend = CELERY_RESULT_BACKEND
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# Optional: explicitly assign SSL configs if used
if broker_use_ssl:
    logger.info("Using SSL for Redis connection")
else:
    logger.info("Not using SSL for Redis connection")
