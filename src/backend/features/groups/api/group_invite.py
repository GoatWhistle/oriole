from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.schemas import GroupInviteCreate, GroupInviteUpdate
from features.groups.services import group_invite as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.post(
    "/{group_id}/invites",
    response_model=SuccessResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_group_invite(
    request: Request,
    group_invite_create: GroupInviteCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_group_invite(
        session, user_id, request, group_invite_create
    )
    return create_json_response(data=data)


@router.get(
    "/invites/{group_invite_id}",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_group_invite_by_id(
    request: Request,
    group_invite_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_group_invite_by_id(
        session, user_id, request, group_invite_id
    )
    return create_json_response(data=data)


@router.get(
    "/{group_id}/invites/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_group_invites_in_group(
    request: Request,
    group_id: int,
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_group_invites_in_group(
        session, user_id, request, group_id, is_active
    )
    return create_json_response(data=data)


@router.put(
    "/invites/{group_invite_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def update_group_invite(
    request: Request,
    group_invite_id: int,
    group_invite_update: GroupInviteUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_group_invite(
        session, user_id, request, group_invite_id, group_invite_update
    )
    return create_json_response(data=data)


@router.delete(
    "/invites/{group_invite_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_group_invite(
    group_invite_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> None:
    await service.delete_group_invite(session, user_id, group_invite_id)


@router.delete(
    "/{group_id}/invites/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_group_invites_in_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> None:
    await service.delete_group_invites_in_group(session, user_id, group_id)
