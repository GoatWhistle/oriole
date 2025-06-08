from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.redis import redis_connection
from database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connection.connect()

    yield

    await redis_connection.close()
    await db_helper.dispose()
