from fastapi import APIRouter

from .account import router as account_router
from .module import router as module_router

router = APIRouter()

router.include_router(router=account_router)
router.include_router(router=module_router)
