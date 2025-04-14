from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from core.config import settings
from core.models import db_helper
from core.models.user import User
from api.api_v1.fastapi_users import (
    fastapi_users,
    current_active_user,
)

from core.exceptions.user import (
    get_user_or_404,
    check_teacher_or_403,
)

from core.schemas.user import (
    UserRead,
    UserUpdate,
    UserProfileUpdatePartial,
)

from core.schemas.assignment import AssignmentRead
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead

from crud import users as crud

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
    return await crud.get_user(session=session, user_id=user_id)


@router.patch(
    "/{user_id}/profile",
    response_model=UserRead,
)
async def update_user_profile(
    user_id: int,
    profile_update: UserProfileUpdatePartial,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this profile",
        )

    return await crud.update_user(
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
    return await crud.get_user_groups(session=session, user_id=user_id)


@router.get(
    "/{user_id}/assignments",
    response_model=Sequence[AssignmentRead],
)
async def read_user_assignments(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_user_assignments(session=session, user_id=user_id)


@router.get(
    "/{user_id}/tasks",
    response_model=Sequence[TaskRead],
)
async def read_user_tasks(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_user_tasks(session=session, user_id=user_id)


@router.post(
    "/{user_id}/groups/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_user_group(
    user_id: int,
    group_id: int,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.add_user_to_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
        current_user=current_user,
    )


@router.delete(
    "/{user_id}/groups/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_from_group(
    user_id: int,
    group_id: int,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await check_teacher_or_403(session, user_id)

    await crud.remove_user_from_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
