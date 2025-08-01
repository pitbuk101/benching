from celery import Celery
from src.celery_tasks import celeryconfig

celery_app = Celery("chat_service")
celery_app.config_from_object(celeryconfig)
celery_app.autodiscover_tasks(["src.celery_tasks"])


