import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from api import router as api_router
from core.config import settings
from core.events import lifespan
from middlewares import (
    LoggingMiddleware,
    AutoCacheMiddleware,
    ExceptionHandlerMiddleware,
)

app = FastAPI(lifespan=lifespan)

if settings.redis.limiter_enabled:
    app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.add_middleware(ExceptionHandlerMiddleware)

app.include_router(
    api_router,
)


@app.get("/api/ping")
def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(
        "main:backend",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
