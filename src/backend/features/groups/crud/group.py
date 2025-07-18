from typing import Sequence, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.accounts.models import Account
from features.groups.models import Group
from features.groups.schemas import GroupCreate


async def create_group(
    session: AsyncSession,
    group_create: GroupCreate,
    creator_id: int,
) -> Group:
    group = Group(
        **group_create.model_dump(),
        creator_id=creator_id,
    )
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group


async def get_group_by_id(
    session: AsyncSession,
    group_id: int,
) -> Group | None:
    return await session.get(Group, group_id)


async def get_groups_by_ids(
    session: AsyncSession,
    group_ids: list[int],
) -> list[Group]:
    if not group_ids:
        return []
    statement = select(Group).where(Group.id.in_(group_ids))
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_groups_by_account_ids(
    session: AsyncSession,
    account_ids: Sequence[int],
) -> list[Group]:
    result = await session.execute(
        select(Group).join(Account).where(Account.id.in_(account_ids))
    )
    return list(result.scalars().all())


async def update_group(
    session: AsyncSession,
    group: Group,
    group_update: dict[str, Any],
) -> Group:
    for key, value in group_update.items():
        setattr(group, key, value)
    await session.commit()
    await session.refresh(group)
    return group


async def delete_group(
    session: AsyncSession,
    group: Group,
) -> None:
    await session.delete(group)
    await session.commit()
