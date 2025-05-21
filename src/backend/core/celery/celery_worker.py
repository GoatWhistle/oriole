from celery import Celery
from core.config import settings
from typing import Coroutine, Any
import json
from kombu.serialization import register
import asyncio
import logging
import redis

logger = logging.getLogger(__name__)


class CeleryConfig:
    def __init__(self):
        self.redis_host = self._get_redis_host()
        self.redis_port = self._get_redis_port()
        self._test_redis_connection()

    def _get_redis_host(self) -> str:

        host = getattr(
            settings.redis, "host", getattr(settings.redis, "url", "localhost")
        )
        if "://" in host:
            host = host.split("://")[1].split("/")[0].split(":")[0]
        return host

    def _get_redis_port(self) -> int:
        port = getattr(settings.redis, "port", 6379)
        if isinstance(port, str):
            if not port.isdigit():
                raise ValueError(f"Invalid Redis port: {port}")
            port = int(port)
        return port

    def _test_redis_connection(self):
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=0,
                socket_connect_timeout=3,
            )
            if not r.ping():
                raise ConnectionError("Redis connection failed")
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            raise

    def get_redis_url(self, db: int = 0) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{db}"


def sync_run_async(coro: Coroutine) -> Any:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def encode_async(obj: Any) -> str:
    try:
        if isinstance(obj, Coroutine):
            obj = sync_run_async(obj)
        return json.dumps(obj, default=str)
    except Exception as e:
        logger.error(f"Serialization failed: {e}")
        raise ValueError(f"Serialization error: {e}")


def decode_async(obj: str) -> Any:
    try:
        return json.loads(obj)
    except json.JSONDecodeError as e:
        logger.error(f"Deserialization failed: {e}")
        raise ValueError(f"Invalid JSON: {e}")


try:
    celery_config = CeleryConfig()
    broker_url = celery_config.get_redis_url(0)
    backend_url = celery_config.get_redis_url(1)
except Exception as e:
    logger.critical(f"Celery configuration failed: {e}")
    raise

register(
    "async_serializer",
    encode_async,
    decode_async,
    content_type="application/x-async-json",
    content_encoding="utf-8",
)

celery_app = Celery(
    "worker",
    broker=broker_url,
    backend=backend_url,
    include=["core.celery.tasks", "core.celery.assignments"],
)

celery_app.conf.update(
    task_serializer="async_serializer",
    result_serializer="async_serializer",
    accept_content=["json", "async_serializer"],
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=5,
    task_default_queue="default",
    worker_pool="solo",
    task_always_eager=False,
    worker_redirect_stdouts=False,
    worker_hijack_root_logger=False,
    broker_transport_options={
        "visibility_timeout": 3600,
        "health_check_interval": 30,
        "socket_keepalive": True,
        "socket_timeout": 10,
        "retry_on_timeout": True,
    },
    result_backend_transport_options={
        "retry_policy": {
            "timeout": 5.0,
            "interval_start": 0.1,
            "interval_step": 0.2,
            "interval_max": 1.0,
            "max_retries": 3,
        }
    },
)

if getattr(settings, "celery", None) and getattr(
    settings.celery, "beat_enabled", False
):
    try:
        celery_app.conf.update(
            beat_scheduler="redbeat.RedBeatScheduler",
            redbeat_redis_url=celery_config.get_redis_url(2),
            redbeat_key_prefix="redbeat:",
            redbeat_lock_timeout=60,
            beat_schedule={
                "check-task-deadlines": {
                    "task": "core.celery.tasks.check_deadlines",
                    "schedule": 60.0,  # 5 минут
                    "options": {"expires": 300, "queue": "default"},
                },
                "check-assignment-deadlines": {
                    "task": "core.celery.assignments.check_deadlines",
                    "schedule": 60.0,  # 1 час
                },
            },
        )
        logger.info("Celery Beat scheduler configured")
    except Exception as e:
        logger.error(f"Failed to configure Celery Beat: {e}")
        raise

logger.info("Celery application initialized successfully")
