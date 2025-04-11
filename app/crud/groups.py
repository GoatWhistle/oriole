from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.assignment import AssignmentRead
from core.schemas.user import UserRead

from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)

from core.models import (
    Assignment,
    Group,
    UserProfile,
)


async def create_group(
    session: AsyncSession,
    group_in: GroupCreate,
) -> GroupRead:
    group = Group(**group_in.model_dump())
    session.add(group)
    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def get_group(
    session: AsyncSession,
    group_id: int,
) -> GroupRead | None:
    group = await session.get(Group, group_id)

    return None if group is None else GroupRead.model_validate(group)


async def get_groups(
    session: AsyncSession,
    user_id: int,
) -> Sequence[GroupRead]:
    statement = (
        select(Group)
        .join(Group.users)
        .where(UserProfile.user_id == user_id)
        .order_by(Group.id)
    )

    result: Result = await session.execute(statement)
    groups = list(result.scalars().all())

    return [GroupRead.model_validate(group) for group in groups]


async def get_users_in_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[UserRead]:
    statement = select(UserProfile).join(UserProfile.groups).where(Group.id == group_id)

    result: Result = await session.execute(statement)
    users = list(result.scalars().all())

    return [UserRead.model_validate(user) for user in users]


async def get_assignments_in_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[AssignmentRead]:
    statement = (
        select(Assignment)
        .where(Assignment.group_id == group_id)
        .order_by(Assignment.id)
    )

    result = await session.execute(statement)
    assignments = list(result.scalars().all())

    return [AssignmentRead.model_validate(assignment) for assignment in assignments]


async def update_group(
    session: AsyncSession,
    group: GroupRead,
    group_update: GroupUpdate | GroupUpdatePartial,
    partial: bool = False,
) -> GroupRead:
    for name, value in group_update.model_dump(exclude_unset=partial).items():
        setattr(group, name, value)

    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def delete_group(
    session: AsyncSession,
    group: GroupRead,
) -> None:
    await session.delete(group)
    await session.commit()
