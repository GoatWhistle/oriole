from fastapi import APIRouter

from .account import router as account_router

router = APIRouter()

router.include_router(router=account_router)
