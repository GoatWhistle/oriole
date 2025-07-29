from fastapi import APIRouter

from .base import router as base_task_router
from .code import router as code_task_router
from .string_match import router as string_match_task_router
from .choice import router as multiple_choice_task_router


router = APIRouter()

router.include_router(router=base_task_router, prefix="/base")
router.include_router(router=string_match_task_router, prefix="/string-match")
router.include_router(router=code_task_router, prefix="/code")
router.include_router(router=multiple_choice_task_router, prefix="/multiple-choice")
