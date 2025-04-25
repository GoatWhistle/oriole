import uvicorn

from fastapi import FastAPI

from core.models import lifespan
from core.config import settings

from api import router as api_router

app = FastAPI(lifespan=lifespan)

app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
