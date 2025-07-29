from fastapi import APIRouter
from .feedback_multiple_task import router as multiple_choice_feedback


router = APIRouter()


router.include_router(
    router=multiple_choice_feedback, prefix="/feedback-multiple-choice"
)
