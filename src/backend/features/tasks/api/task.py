from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.tasks.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskUpdatePartial,
)
from features.tasks.services import string_match as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_string_match_task(session, user_id, task_in)
    return create_json_response(data=data)


@router.get(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    include: list[str] | None = Query(None),
):
    data = await service.get_task_by_id(session, user_id, task_id, include)
    return create_json_response(data=data)


@router.get(
    "/",
    response_model=list[SuccessListResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_tasks(
    request: Request,
    is_active: bool | None = None,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    include: list[str] | None = Query(None),
):
    data = await service.get_user_tasks(session, user_id, is_active, include)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/tasks/?is_active={is_active if is_active else False}",
        include=include,
    )


@router.put(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_update: TaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_task(session, user_id, task_id, task_update, False)
    return create_json_response(data=data)


@router.patch(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_task_partial(
    task_update: TaskUpdatePartial,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_task(session, user_id, task_id, task_update, True)
    return create_json_response(data=data)


@router.delete(
    "/{task_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.delete_task(session, user_id, task_id)
