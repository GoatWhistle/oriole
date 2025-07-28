from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.services.choice as solution_service
import features.tasks.services.choice as task_choice_service
from database import db_helper
from features.solutions.schemas import MultipleChoiceSolutionCreate
from features.tasks.schemas import MultipleChoiceTaskUpdate, MultipleChoiceTaskCreate
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_multiple_choice_task(
    task_create: MultipleChoiceTaskCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_choice_service.create_multiple_choice_task(session, user_id, task_create)
    return create_json_response(data=data)


@router.put(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def update_multiple_choice_task(
    task_update: MultipleChoiceTaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_choice_service.update_multiple_choice_task(
        session, user_id, task_id, task_update
    )
    return create_json_response(data=data)


@router.post(
    "/{task_id}/solutions",
    response_model=SuccessResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_multiple_choice_solution(
    solution_create: MultipleChoiceSolutionCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.create_multiple_choice_solution(
        session, user_id, solution_create
    )
    return create_json_response(data=data)
