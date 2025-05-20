from celery import Celery
from core.config import settings
from typing import Coroutine, Any
import json
from kombu.serialization import register
import asyncio
import logging

# Настройка логгера
logger = logging.getLogger(__name__)


def encode_async(obj: Any) -> str:
    """
    Кастомный сериализатор для Celery, обрабатывающий:
    - Асинхронные корутины
    - Стандартные JSON-сериализуемые объекты
    - Сложные объекты через str()
    """
    try:
        # Обработка асинхронных корутин
        if isinstance(obj, Coroutine):
            try:
                # Получаем или создаем event loop
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                obj = loop.run_until_complete(obj)
            except RuntimeError as e:
                logger.error(f"Event loop error: {e}")
                raise ValueError(f"Async operation failed: {e}")

        # Стандартная JSON-сериализация
        try:
            return json.dumps(
                obj, default=str
            )  # Используем default=str для сложных объектов
        except (TypeError, ValueError) as e:
            logger.warning(f"JSON serialization fallback for {type(obj)}: {e}")
            return json.dumps(str(obj))
    except Exception as e:
        logger.error(f"Serialization failed: {e}")
        raise ValueError(f"Serialization error: {e}")


def decode_async(obj: str) -> Any:
    """Десериализация JSON строки"""
    try:
        return json.loads(obj)
    except json.JSONDecodeError as e:
        logger.error(f"Deserialization failed: {e}")
        raise ValueError(f"Invalid JSON: {e}")


# Регистрация кастомного сериализатора
register(
    "async_serializer",
    encode_async,
    decode_async,
    content_type="application/x-async-json",
    content_encoding="utf-8",
)

# Инициализация Celery приложения
celery_app = Celery(
    "core.celery.celery_worker",
    broker=f"redis://{settings.redis.host}:{settings.redis.port}/0",  # Явный redis://
    backend=f"redis://{settings.redis.host}:{settings.redis.port}/1",
    include=[
        "core.celery.tasks",
        "core.celery.assignments",
    ],  # Проверьте существование этих модулей
)

# Конфигурация Celery
celery_app.conf.update(
    # Настройки сериализации
    task_serializer="async_serializer",
    result_serializer="async_serializer",
    accept_content=["json", "async_serializer"],
    # Оптимизация работы
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=3,
    task_default_queue="default",
    # Настройки для работы с асинхронными задачами
    worker_pool="solo",
    task_always_eager=False,
    # Логирование
    worker_redirect_stdouts=False,
    worker_hijack_root_logger=False,
)

# Настройки для beat (если используется)
celery_app.conf.beat_scheduler = "redbeat.RedBeatScheduler"
celery_app.conf.redbeat_redis_url = (
    f"redis://{settings.redis.host}:{settings.redis.port}/2"
)
