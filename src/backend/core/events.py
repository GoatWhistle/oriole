from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.redis import redis_connection
from database import db_helper
from core.logging.config import setup_logging

from middlewares.limiter import limiter
from core.config import settings
from middlewares.limiter import universal_rate_limit_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.redis.limiter_enabled:
        app.state.limiter = limiter
        app.add_exception_handler(Exception, universal_rate_limit_handler)

    await redis_connection.connect()
    setup_logging()

    yield

    await redis_connection.close()
    await db_helper.dispose()
