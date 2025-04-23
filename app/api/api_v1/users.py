from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from core.config import settings
from core.models import db_helper
from core.schemas.user import (
    UserRead,
    UserUpdate,
    UserUpdatePartial,
)
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead
from core.schemas.assignment import AssignmentRead
from core.schemas.account import AccountRole

from crud import users as crud
from crud.auth import get_current_active_auth_user_id

router = APIRouter(
    tags=["Users"],
    prefix=settings.api.v1.users,
)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate | UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user(session, user_id, user_data, current_user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user(
        session, user_id, user_update, current_user_id, partial=True
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    await crud.delete_user(session, current_user_id, user_id)


@router.get("/{user_id}/groups", response_model=Sequence[GroupRead])
async def get_user_groups(
    user_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.get_user_groups(session, user_id, current_user_id)


@router.get("/{user_id}/assignments", response_model=Sequence[AssignmentRead])
async def get_user_assignments(
    user_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.get_user_assignments(session, user_id, current_user_id)


@router.get("/{user_id}/tasks", response_model=Sequence[TaskRead])
async def get_user_tasks(
    user_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.get_user_tasks(session, user_id, current_user_id)


@router.delete("/{user_id}/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_group(
    deleted_user_id: int,
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    admin_user_id: int = Depends(get_current_active_auth_user_id),
):
    await crud.remove_user_from_group(
        session=session,
        admin_user_id=admin_user_id,
        deleted_user_id=deleted_user_id,
        group_id=group_id,
    )


@router.patch("/{user_id}/groups/{group_id}/role")
async def change_user_role_in_group(
    role_user_id: int,
    group_id: int,
    new_role: AccountRole,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    admin_user_id: int = Depends(get_current_active_auth_user_id),
):
    await crud.change_user_role_in_group(
        session=session,
        admin_user_id=admin_user_id,
        role_user_id=role_user_id,
        group_id=group_id,
        new_role=new_role,
    )
