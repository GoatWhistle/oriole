from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from watchfiles import awatch

from core.config import settings
from core.models import db_helper, User

from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)

from crud import groups as crud

from core.schemas.assignment import AssignmentRead
from core.schemas.user import UserRead

router = APIRouter(tags=[settings.api.v1.groups[1:].capitalize()])


# TODO: import get_current_user
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
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_in: GroupCreate,
):
    return await crud.create_group(
        session=session,
        user=current_user,
        group_in=group_in,
    )


# TODO: import get_current_user
@router.get(
    "/{group_id}/",
    response_model=GroupRead,
)
async def get_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
):
    return await crud.get_group(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
    )


# TODO: import get_current_user
@router.get(
    "/",
    response_model=Sequence[GroupRead],
)
async def get_groups(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await crud.get_groups(session=session, user_id=current_user.id)


# TODO: import get_current_user
@router.put("/{group_id}/")
async def update_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
    group_update: GroupUpdate,
):
    return await crud.update_group(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
        group_update=group_update,
        partial=False,
    )


# TODO: import get_current_user
@router.patch("/{group_id}/")
async def update_group_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
    group_update: GroupUpdatePartial,
):
    return await crud.update_group(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
        group_update=group_update,
        partial=True,
    )


# TODO: import get_current_user
@router.delete(
    "/{group_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
) -> None:
    await crud.delete_group(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
    )


# TODO: import get_current_user
@router.get(
    "/{group_id}/users/",
    response_model=Sequence[UserRead],
)
async def get_users_in_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
):
    return await crud.get_users_in_group(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
    )


# TODO: import get_current_user
@router.get(
    "/{group_id}/assignments/",
    response_model=Sequence[AssignmentRead],
)
async def get_assignments_in_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
):
    return await crud.get_assignments_in_group(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
    )


# TODO: import get_current_user
@router.get("/{group_id}/create_link/")
async def create_link(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    group_id: int,
):
    return await crud.create_link(
        session=session,
        user_id=current_user.id,
        group_id=group_id,
    )
