from fastapi import APIRouter

from .notification import router as notification_router

router = APIRouter()

router.include_router(router=notification_router, prefix="/notification")
