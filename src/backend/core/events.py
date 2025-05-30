from fastapi import FastAPI
from core.redis import redis_connection
from core.models.db_helper import db_helper
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connection.connect()

    yield

    await redis_connection.close()
    await db_helper.dispose()


