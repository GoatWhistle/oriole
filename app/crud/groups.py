from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.group import check_group_exists

from core.schemas.assignment import AssignmentRead
from core.schemas.user import UserRead

from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)

from core.models import (
    Account,
    Assignment,
    Group,
    User,
)


async def create_group(
    session: AsyncSession,
    group_in: GroupCreate,
) -> GroupRead:
    group = Group(**group_in.model_dump(exclude={"accounts", "assignments"}))
    session.add(group)

    if group_in.accounts:
        users = await session.execute(
            select(User).where(User.id.in_(group_in.accounts))
        )
        existing_users = users.scalars().all()

        for user in existing_users:
            account = Account(user_id=user.id, group_id=group.id)
            group.accounts.append(account)

    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def get_group(
    session: AsyncSession,
    group_id: int,
) -> GroupRead:
    await check_group_exists(session=session, group_id=group_id)
    group = await session.get(Group, group_id)

    return GroupRead.model_validate(group)


async def get_groups(
    session: AsyncSession,
    user_id: int,
) -> Sequence[GroupRead]:
    statement = (
        select(Group).join(Account).where(Account.user_id == user_id).order_by(Group.id)
    )

    result: Result = await session.execute(statement)
    groups = list(result.scalars().all())

    return [GroupRead.model_validate(group) for group in groups]


async def update_group(
    session: AsyncSession,
    group_id: int,
    group_update: GroupUpdate | GroupUpdatePartial,
    partial: bool = False,
) -> GroupRead:
    await check_group_exists(session=session, group_id=group_id)
    group = await session.get(Group, group_id)

    for key, value in group_update.model_dump(exclude_unset=partial).items():
        setattr(group, key, value)

    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def delete_group(
    session: AsyncSession,
    group_id: int,
) -> None:
    await check_group_exists(session=session, group_id=group_id)
    group = await session.get(Group, group_id)
    await session.delete(group)
    await session.commit()


async def get_users_in_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[UserRead]:
    statement = select(User).join(Account).where(Account.group_id == group_id)

    result = await session.execute(statement)
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
