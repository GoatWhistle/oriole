from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)
from features.groups.services import group as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
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
    response_model=GroupRead,
    status_code=status.HTTP_200_OK,
)
async def get_group_by_id(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    include: list[str] | None = Query(None),
):
    data = await service.get_group_by_id(session, user_id, group_id, include)
    return create_json_response(data=data)


@router.get(
    "/",
    response_model=list[SuccessListResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_groups(
    page: int | None = None,
    per_page: int | None = None,
    include: list[str] | None = Query(None),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_user_groups(session, user_id, include)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url="http://127.0.0.1:8000/api/groups/",
        include=include,
    )


@router.put(
    "/{group_id}/",
    response_model=SuccessResponse[GroupRead],
    status_code=status.HTTP_200_OK,
)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_group(session, user_id, group_id, group_update, False)
    return create_json_response(data=data)


@router.patch(
    "/{group_id}/",
    response_model=SuccessResponse[GroupRead],
    status_code=status.HTTP_200_OK,
)
async def update_group_partial(
    group_id: int,
    group_update: GroupUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_group(session, user_id, group_id, group_update, True)
    return create_json_response(data=data)


@router.delete(
    "/{group_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.delete_group(session, user_id, group_id)


@router.get(
    "/{group_id}/users/",
    response_model=list[SuccessListResponse[GroupRead]],
    status_code=status.HTTP_200_OK,
)
async def get_users_in_group(
    group_id: int,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_users_in_group(session, user_id, group_id)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"http://127.0.0.1:8000/api/groups/{group_id}/users/",
    )
