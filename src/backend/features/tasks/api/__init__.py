from fastapi import APIRouter

from .base import router as base_task_router
from .string_match import router as string_match_task_router

router = APIRouter()

router.include_router(router=base_task_router)
router.include_router(router=string_match_task_router)
