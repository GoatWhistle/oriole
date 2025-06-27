from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.schemas.invite import LinkRead, LinkJoinRead
from features.groups.services import invite as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse

router = APIRouter()


@router.post(
    "/{group_id}/invite/",
    response_model=SuccessResponse[LinkRead],
    status_code=status.HTTP_200_OK,
)
async def invite_user(
    request: Request,
    group_id: int,
    expires_minutes: int = 30,
    single_use: bool = False,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.invite_user(
        session, user_id, request, group_id, expires_minutes, single_use
    )
    return create_json_response(data=data)


@router.post(
    "/join/{invite_code}",
    response_model=SuccessResponse[LinkJoinRead],
    status_code=status.HTTP_200_OK,
)
async def join_by_link(
    invite_code: str,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.join_by_link(session, user_id, invite_code)
    return create_json_response(data=data)


@router.delete(
    "/{group_id}/delete-invites/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group_invites(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> None:
    await service.delete_group_invites(session, user_id, group_id)
