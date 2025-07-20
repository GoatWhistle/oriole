import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import os

from api import router as api_router
from core.config import settings
from core.events import lifespan
from middlewares import (
    LoggingMiddleware,
    AutoCacheMiddleware,
    ExceptionHandlerMiddleware,
)


is_dev = os.getenv("IS_DEV", "false").lower() == "true"

sentry_sdk.init(
    dsn=settings.sentry.dsn,
    send_default_pii=True,
)

app = FastAPI(lifespan=lifespan)

app.add_middleware(ExceptionHandlerMiddleware)

app.add_middleware(SentryAsgiMiddleware)

Instrumentator().instrument(app).expose(app)

if settings.redis.limiter_enabled:
    app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not (is_dev):
    app.add_middleware(
        AutoCacheMiddleware,
        ttl=600,
        exclude_paths=[
            "docs",
            "openapi.json",
            "redoc",
            "static",
            "docs#",
        ],
        invalidate_paths=["auth", "verify"],
    )
app.add_middleware(LoggingMiddleware)

app.include_router(
    api_router,
)


@app.get("/api/ping")
async def ping():
    a = 2 + ""
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
