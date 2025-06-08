from typing import Annotated

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.services import invite as service
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.post(
    "/{group_id}/invite/",
    status_code=status.HTTP_200_OK,
)
async def invite_user(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_id: int,
    expires_minutes: int = 30,
    single_use: bool = False,
):
    return await service.invite_user(
        session=session,
        user_id=user_id,
        request=request,
        group_id=group_id,
        expires_minutes=expires_minutes,
        single_use=single_use,
    )


@router.post(
    "/join/{invite_code}",
    status_code=status.HTTP_200_OK,
)
async def join_by_link(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    invite_code: str,
):
    return await service.join_by_link(
        session=session,
        user_id=user_id,
        invite_code=invite_code,
    )


@router.delete(
    "/{group_id}/delete-invites/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group_invites(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_id: int,
) -> None:
    await service.delete_group_invites(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
