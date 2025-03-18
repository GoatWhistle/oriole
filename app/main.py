from fastapi import FastAPI
import uvicorn

from app.core.models import lifespan
from core.config import settings

app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
