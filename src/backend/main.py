import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.events import lifespan
from core.config import settings
from core.redis import AutoCacheMiddleware
from core.logging import LoggingMiddleware

from api import router as api_router

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://frontend:80",
        "http://127.0.0.1:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AutoCacheMiddleware,
    ttl=1200,
    exclude_paths=["auth", "verify"]
)
app.add_middleware(LoggingMiddleware)


app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:backend",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
