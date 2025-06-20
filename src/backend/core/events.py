from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.redis import redis_connection
from database import db_helper

from middlewares.limiter import limiter
from slowapi.errors import RateLimitExceeded
from core.config import settings
from middlewares.limiter import custom_rate_limit_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.redis.limiter_enabled:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

    await redis_connection.connect()

    yield

    await redis_connection.close()
    await db_helper.dispose()
