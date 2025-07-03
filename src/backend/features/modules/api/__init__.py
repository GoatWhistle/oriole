from fastapi import APIRouter

from .module import router as module_router
from .task import router as task_router

router = APIRouter()

router.include_router(router=module_router)
router.include_router(router=task_router)
