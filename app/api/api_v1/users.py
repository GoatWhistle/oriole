from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from core.config import settings
from core.models import db_helper
from core.models.user import User
from api.api_v1.fastapi_users import fastapi_users

from core.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserProfileUpdatePartial,
)

from core.schemas.assignment import AssignmentRead
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead

from crud.users import (
    get_user,
    update_user,
    get_user_groups,
    get_user_assignments,
    get_user_tasks,
    add_user_to_group,
    remove_user_from_group,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)


@router.get(
    "/{user_id}/",
    response_model=UserRead,
)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await get_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return UserRead.from_orm(user)


@router.patch(
    "/{user_id}/profile",
    response_model=UserRead,
)
async def update_user_profile(
    user_id: int,
    profile_update: UserProfileUpdatePartial,
    current_user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this profile",
        )

    return await update_user(
        session=session,
        user_id=user_id,
        user_update=profile_update,
        partial=True,
    )


@router.get(
    "/{user_id}/groups",
    response_model=Sequence[GroupRead],
)
async def read_user_groups(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await get_user_groups(session=session, user_id=user_id)


@router.get(
    "/{user_id}/assignments",
    response_model=Sequence[AssignmentRead],
)
async def read_user_assignments(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await get_user_assignments(session=session, user_id=user_id)


@router.get(
    "/{user_id}/tasks",
    response_model=Sequence[TaskRead],
)
async def read_user_tasks(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await get_user_tasks(session=session, user_id=user_id)


@router.post(
    "/{user_id}/groups/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_user_group(
    user_id: int,
    group_id: int,
    current_user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission, only admin can do",
        )

    await add_user_to_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )


@router.delete(
    "/{user_id}/groups/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_group(
    user_id: int,
    group_id: int,
    current_user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="",
        )

    await remove_user_from_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
