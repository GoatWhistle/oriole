from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.schemas.group import (
    GroupCreate,
    GroupUpdate,
)
from features.groups.services import group as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_group(
    group_in: GroupCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_group(session, user_id, group_in)
    return create_json_response(data=data)


@router.get(
    "/{group_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    include: list[str] | None = Query(None),
):
    data = await service.get_group(session, user_id, group_id, include)
    return create_json_response(data=data)


@router.get(
    "/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_user_groups(
    request: Request,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_user_groups(session, user_id)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/groups/",
    )


@router.put(
    "/{group_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_group(session, user_id, group_id, group_update)
    return create_json_response(data=data)


@router.delete(
    "/{group_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.delete_group(session, user_id, group_id)
