from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.schemas.account import AccountRoleChangeRead
from features.groups.services import account as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse

router = APIRouter()


@router.patch(
    "/{group_id}/promote/{promote_user_id}/",
    response_model=SuccessResponse[AccountRoleChangeRead],
    status_code=status.HTTP_200_OK,
)
async def promote_user_to_admin(
    promote_user_id: int,
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.promote_user_to_admin(
        session, user_id, promote_user_id, group_id
    )
    return create_json_response(data=data)


@router.patch(
    "/{group_id}/demote/{demote_user_id}/",
    response_model=SuccessResponse[AccountRoleChangeRead],
    status_code=status.HTTP_200_OK,
)
async def demote_user_to_member(
    demote_user_id: int,
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.demote_user_to_member(
        session, user_id, demote_user_id, group_id
    )
    return create_json_response(data=data)


@router.delete(
    "/{group_id}/kick/{remove_user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_from_group(
    remove_user_id: int,
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.remove_user_from_group(session, user_id, remove_user_id, group_id)


@router.delete(
    "/{group_id}/leave/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def leave_from_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.leave_from_group(session, user_id, group_id)
