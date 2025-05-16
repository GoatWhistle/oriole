from celery import Celery

from core.config import settings

celery = Celery(
    __name__,
    broker=f"{settings.redis.url}{settings.redis.port}/0",
    backend=f"{settings.redis.url}{settings.redis.port}/1"
)

#celery.autodiscover_tasks(['tasks'])