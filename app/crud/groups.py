from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Group, User
from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)


async def create_group(
    session: AsyncSession,
    group_in: GroupCreate,
) -> GroupRead:
    group = GroupRead(**group_in.model_dump())
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group


async def get_groups(
    session: AsyncSession,
) -> Sequence[Group]:
    statement = select(Group).order_by(Group.id)
    result: Result = await session.execute(statement)
    return list(result.scalars().all())


async def get_group(
    session: AsyncSession,
    group_id: int,
) -> Group | None:
    return await session.get(Group, group_id)


async def get_users_in_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[User]:
    statement = select(User).join(User.groups).where(Group.id == group_id)
    result: Result = await session.execute(statement)
    return list(result.scalars().all())


async def update_group(
    session: AsyncSession,
    group: Group,
    group_update: GroupUpdate | GroupUpdatePartial,
    partial: bool = False,
) -> Group:
    for name, value in group_update.model_dump(exclude_unset=partial).items():
        setattr(group, name, value)
    await session.commit()
    return group


async def delete_group(
    session: AsyncSession,
    group: Group,
) -> None:
    await session.delete(group)
    await session.commit()
