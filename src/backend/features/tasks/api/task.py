from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.tasks.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
)
from features.tasks.services import task as service
from features.users.services.auth import get_current_active_auth_user_id
from utils import get_current_utc
from utils.response_func import create_list_response
from utils.schemas import SuccessResponse, Meta, SuccessListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_task(session, user_id, task_in)
    response_content = jsonable_encoder(
        SuccessResponse[TaskRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.get(
    "/{task_id}/",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_task_by_id(session, user_id, task_id)
    response_content = jsonable_encoder(
        SuccessResponse[TaskRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.get(
    "/",
    response_model=list[SuccessListResponse[TaskRead]],
    status_code=status.HTTP_200_OK,
)
async def get_user_tasks(
    is_active: bool | None = None,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_user_tasks(session, user_id, is_active)
    response_content = create_list_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"http://127.0.0.1:8000/api/tasks/?is_active={is_active}",
    )
    return JSONResponse(content=response_content, status_code=200)


@router.put(
    "/{task_id}/",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_update: TaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_task(session, user_id, task_id, task_update, False)
    response_content = jsonable_encoder(
        SuccessResponse[TaskRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.patch(
    "/{task_id}/",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def update_task_partial(
    task_update: TaskUpdatePartial,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_task(session, user_id, task_id, task_update, True)
    response_content = jsonable_encoder(
        SuccessResponse[TaskRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


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
