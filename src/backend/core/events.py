from fastapi import FastAPI
from core.redis import redis_connection
from core.models.db_helper import db_helper
from contextlib import asynccontextmanager
from .backgorund_tasks import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connection.connect()
    if not scheduler.running:
        scheduler.start()

    yield

    if scheduler.running:
        scheduler.shutdown(wait=False)
    await redis_connection.close()
    await db_helper.dispose()


