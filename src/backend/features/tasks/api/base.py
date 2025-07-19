from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.solutions.services import base as solution_service
from features.tasks.services import base as task_service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.get(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_task(
    task_id: int,
    include: list[str] | None = Query(None),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_service.get_task(session, user_id, task_id, include)
    return create_json_response(data=data)


@router.get(
    "/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_user_tasks(
    request: Request,
    is_active: bool | None = None,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_service.get_user_tasks(session, user_id, is_active)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/tasks/base/?is_active={is_active if is_active else False}",
    )


@router.delete(
    "/{task_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await task_service.delete_task(session, user_id, task_id)


@router.get(
    "/solutions/{solution_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_solution(
    solution_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.get_solution_by_id(session, user_id, solution_id)
    return create_json_response(data=data)


@router.get(
    "/{task_id}/solutions",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_solutions_in_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.get_solutions_in_task(session, user_id, task_id)
    return create_json_response(data=data)


@router.delete(
    "/solutions/{solution_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_solution(
    solution_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await solution_service.delete_solution(session, user_id, solution_id)
