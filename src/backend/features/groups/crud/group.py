from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import Account
from features.groups.models import Group
from features.groups.schemas import GroupCreate, GroupUpdate, GroupUpdatePartial


async def create_group(
    session: AsyncSession,
    group_in: GroupCreate,
) -> Group:
    group = Group(**group_in.model_dump())
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group


async def get_group_by_id(
    session: AsyncSession,
    group_id: int,
) -> Group | None:
    return await session.get(Group, group_id)


async def get_groups_by_account_ids(
    session: AsyncSession,
    account_ids: Sequence[int],
) -> Sequence[Group]:
    result = await session.execute(
        select(Group).join(Account).where(Account.id.in_(account_ids))
    )
    return result.scalars().all()


async def update_group(
    session: AsyncSession,
    group: Group,
    group_update: GroupUpdate | GroupUpdatePartial,
) -> Group:
    for key, value in group_update.model_dump(exclude_unset=True).items():
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
