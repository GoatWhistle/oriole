from fastapi import APIRouter

from .module import router as module_router

router = APIRouter()

router.include_router(router=module_router)
