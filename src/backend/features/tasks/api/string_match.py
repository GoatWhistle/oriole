from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.services.string_match as solution_service
import features.tasks.services.string_match as service
from database import db_helper
from features.solutions.schemas import StringMatchSolutionCreate
from features.tasks.schemas import (
    StringMatchTaskUpdate,
    StringMatchTaskCreate,
)
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_string_match_task(
    task_in: StringMatchTaskCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_string_match_task(session, user_id, task_in)
    return create_json_response(data=data)


@router.put(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_string_match_task(
    task_update: StringMatchTaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_string_match_task(
        session, user_id, task_id, task_update
    )
    return create_json_response(data=data)


@router.post(
    "/{task_id}/solutions",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_string_match_solution(
    solution_in: StringMatchSolutionCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.create_string_match_solution(
        session, user_id, solution_in
    )
    pass
    return create_json_response(data=data)
