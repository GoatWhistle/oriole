from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from groups.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupReadPartial,
    GroupUpdate,
    GroupUpdatePartial,
)
from groups.services import group as service
from users.crud.auth import get_current_active_auth_user_id
from users.schemas import UserProfileRead

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
    return await service.create_group(
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
    return await service.get_group_by_id(
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
    return await service.get_user_groups(
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
    return await service.update_group(
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
    return await service.update_group(
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
    await service.delete_group(
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
    return await service.get_users_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
