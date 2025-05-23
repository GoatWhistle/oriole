from fastapi import APIRouter, Depends, status, Request

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from core.schemas.assignment import AssignmentReadPartial
from core.schemas.user import UserProfileRead

from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupReadPartial,
    GroupUpdate,
    GroupUpdatePartial,
)

from core.models import db_helper
from crud.auth import get_current_active_auth_user_id
from crud import groups as crud


router = APIRouter()


@router.post(
    "/",
    response_model=GroupRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_in: GroupCreate,
):
    return await crud.create_group(
        session=session,
        user_id=user_id,
        group_in=group_in,
    )


@router.get(
    "/{group_id}/",
    response_model=GroupRead,
    status_code=status.HTTP_200_OK,
)
async def get_group_by_id(
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
    return await crud.get_group_by_id(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )


@router.get(
    "/",
    response_model=Sequence[GroupReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_user_groups(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
):
    return await crud.get_user_groups(
        session=session,
        user_id=user_id,
    )


@router.put(
    "/{group_id}/",
    response_model=GroupRead,
    status_code=status.HTTP_200_OK,
)
async def update_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_id: int,
    group_update: GroupUpdate,
):
    return await crud.update_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
        group_update=group_update,
        is_partial=False,
    )


@router.patch(
    "/{group_id}/",
    response_model=GroupRead,
    status_code=status.HTTP_200_OK,
)
async def update_group_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_id: int,
    group_update: GroupUpdatePartial,
):
    return await crud.update_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
        group_update=group_update,
        is_partial=True,
    )


@router.delete(
    "/{group_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
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
    await crud.delete_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )


@router.get(
    "/{group_id}/users/",
    response_model=Sequence[UserProfileRead],
    status_code=status.HTTP_200_OK,
)
async def get_users_in_group(
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
    return await crud.get_users_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )


@router.get(
    "/{group_id}/assignments/",
    response_model=Sequence[AssignmentReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_assignments_in_group(
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
    return await crud.get_assignments_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )


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
    return await crud.invite_user(
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
    return await crud.join_by_link(
        session=session,
        user_id=user_id,
        invite_code=invite_code,
    )


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
    await crud.promote_user_to_admin(
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
    await crud.demote_user_to_member(
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
    await crud.remove_user_from_group(
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
    await crud.leave_from_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
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
    await crud.delete_group_invites(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
