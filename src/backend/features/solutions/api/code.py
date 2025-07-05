from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.services.code as solution_service
from database import db_helper
from features.solutions.schemas import CodeSolutionCreate
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
)
async def create_code_solution(
    solution_in: CodeSolutionCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.create_code_solution(session, user_id, solution_in)
    return create_json_response(data=data)


@router.get(
    "/{solution_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def get_code_solution_by_id(
    solution_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.get_code_solution_by_id(session, user_id, solution_id)
    return create_json_response(data=data)


@router.get(
    "/",
    response_model=SuccessListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_solutions(
    request: Request,
    task_id: int,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.get_user_solutions_by_task_id(
        session, user_id, task_id
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/solution/code/",
    )
