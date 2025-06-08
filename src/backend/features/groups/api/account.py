from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.services import account as service
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.patch(
    "/{group_id}/promote/{promote_user_id}/",
    status_code=status.HTTP_200_OK,
)
async def promote_user_to_admin(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    promote_user_id: int,
    group_id: int,
):
    await service.promote_user_to_admin(
        session=session,
        user_id=user_id,
        promote_user_id=promote_user_id,
        group_id=group_id,
    )


@router.patch(
    "/{group_id}/demote/{demote_user_id}/",
    status_code=status.HTTP_200_OK,
)
async def demote_user_to_member(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    demote_user_id: int,
    group_id: int,
):
    await service.demote_user_to_member(
        session=session,
        user_id=user_id,
        demote_user_id=demote_user_id,
        group_id=group_id,
    )


@router.delete(
    "/{group_id}/kick/{remove_user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_from_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    remove_user_id: int,
    group_id: int,
):
    await service.remove_user_from_group(
        session=session,
        user_id=user_id,
        remove_user_id=remove_user_id,
        group_id=group_id,
    )


@router.delete(
    "/{group_id}/leave/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def leave_from_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_id: int,
):
    await service.leave_from_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
