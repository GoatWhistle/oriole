from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.models import db_helper
from core.schemas.group import GroupCreate, GroupRead, GroupUpdate, GroupUpdatePartial
from core.schemas.user import UserRead
from crud import groups as crud
from crud.dependencies import validate_group_by_id

router = APIRouter(tags=settings.api.v1.groups.capitalize())


@router.post(
    "/",
    response_model=GroupRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    group_in: GroupCreate,
):
    return await crud.create_group(session=session, group_in=group_in)


@router.get(
    "/{group_id}/",
    response_model=GroupRead,
)
async def get_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    group_id: int,
):
    return await crud.get_group(session=session, group_id=group_id)


@router.get(
    "/",
    response_model=list[GroupRead],
)
async def get_groups(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.get_groups(session=session)


@router.get(
    "/{group_id}/users/",
    response_model=list[UserRead],
)
async def get_users_in_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    group_id: int,
):
    return await crud.get_users_in_group(session=session, group_id=group_id)


@router.put("/{group_id}/")
async def update_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    group_update: GroupUpdate,
    group: Annotated[GroupRead, Depends(validate_group_by_id)],
):
    return await crud.update_group(
        session=session,
        group=group,
        group_update=group_update,
    )


@router.patch("/{group_id}/")
async def update_group_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    group_update: GroupUpdatePartial,
    group: Annotated[GroupRead, Depends(validate_group_by_id)],
):
    return await crud.update_group(
        session=session,
        group=group,
        group_update=group_update,
        partial=True,
    )


@router.delete(
    "/{group_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    group: Annotated[GroupRead, Depends(validate_group_by_id)],
) -> None:
    await crud.delete_group(session=session, group=group)


@router.get("/create_link/{group_id}")
async def create_link(group_id: int):
    await validate_group_by_id(group_id)
    return {"link": f"http://oriole.com/groups/join/{group_id}"}
