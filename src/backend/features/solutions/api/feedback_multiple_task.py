from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.services.feedback_multiple as feedback_service
from database import db_helper
from features.solutions.schemas import MultipleChoiceFeedback
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse


router = APIRouter()


@router.put(
    "/{solution_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def feedback_to_multiple_choice_solution(
    user_id: int,
    feedback_model: MultipleChoiceFeedback,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    data = await feedback_service.create_feedback_multiple_choice_solution(
        session, user_id, feedback_model
    )
    return create_json_response(data=data)