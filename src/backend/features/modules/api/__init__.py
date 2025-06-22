from fastapi import APIRouter

from .copy import router as copy_router
from .module import router as module_router
from .task import router as task_router

router = APIRouter()

router.include_router(router=module_router)
router.include_router(router=task_router)
router.include_router(router=copy_router)
