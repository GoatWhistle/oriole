from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)

from core.exceptions.user import check_user_exists

from core.schemas.account import AccountRole

from core.schemas.assignment import AssignmentRead
from core.schemas.user import UserProfile

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
    user_id: int,
    group_in: GroupCreate,
) -> GroupRead:

    await check_user_exists(session=session, user_id=user_id)

    group = Group(**group_in.model_dump(exclude={"accounts", "assignments"}))

    session.add(group)
    await session.flush()

    admin_account = Account(
        user_id=user_id,
        group_id=group.id,
        role=AccountRole.OWNER.value,
    )
    session.add(admin_account)
    group.accounts.append(admin_account)

    user = await session.get(User, user_id)
    user.profile.accounts.append(admin_account)

    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def get_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> GroupRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    group = await session.get(Group, group_id)
    return GroupRead.model_validate(group)


async def get_groups(
    session: AsyncSession,
    user_id: int,
) -> Sequence[GroupRead]:
    await check_user_exists(session=session, user_id=user_id)

    statement = (
        select(Group).join(Account).where(Account.user_id == user_id).order_by(Group.id)
    )

    result: Result = await session.execute(statement)
    groups = list(result.scalars().all())

    return [GroupRead.model_validate(group) for group in groups]


async def update_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    group_update: GroupUpdate | GroupUpdatePartial,
    partial: bool = False,
) -> GroupRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    group = await session.get(Group, group_id)

    for key, value in group_update.model_dump(exclude_unset=partial).items():
        setattr(group, key, value)

    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def delete_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    group = await session.get(Group, group_id)

    await session.delete(group)
    await session.commit()


async def get_users_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[UserProfile]:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement = select(User).join(Account).where(Account.group_id == group_id)

    result = await session.execute(statement)
    users = list(result.scalars().all())

    return [UserProfile.model_validate(user) for user in users]


async def get_assignments_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[AssignmentRead]:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement = (
        select(Assignment)
        .where(Assignment.group_id == group_id)
        .order_by(Assignment.id)
    )

    result = await session.execute(statement)
    assignments = list(result.scalars().all())

    return [AssignmentRead.model_validate(assignment) for assignment in assignments]


async def create_link(
    session: AsyncSession,
    user_id: int,
    group_id: int,
):
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    return {"link": f"http://oriole.com/join/{group_id}"}
