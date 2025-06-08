from fastapi import APIRouter

from core.config import settings
from .copy import router as copy_router
from .deadline import router as deadline_router
from .module import router as module_router
from .task import router as task_router

router = APIRouter(prefix=settings.api.modules)

router.include_router(router=copy_router)
router.include_router(router=deadline_router)
router.include_router(router=module_router)
router.include_router(router=task_router)
