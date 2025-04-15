from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)
from core.schemas.account import AccountRole

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
    user: User,
    group_in: GroupCreate,
) -> GroupRead:

    group = Group(**group_in.model_dump(exclude={"accounts", "assignments"}))
    group.admin_id = user.id

    session.add(group)
    await session.flush()

    admin_account = Account(
        user_id=user.id, group_id=group.id, role=AccountRole.TEACHER.value
    )

    session.add(admin_account)
    group.accounts.append(admin_account)
    user.profile.accounts.append(admin_account)

    if group_in.accounts:
        result = await session.execute(
            select(User).where(User.id.in_(group_in.accounts))
        )
        existing_users = result.scalars().all()

        for existing_user in existing_users:
            if existing_user.id == user.id:
                continue

            account = Account(
                user_id=existing_user.id,
                group_id=group.id,
                role=AccountRole.STUDENT.value,
            )
            session.add(account)
            group.accounts.append(account)
            existing_user.profile.accounts.append(account)

    await session.commit()
    await session.refresh(group)

    return GroupRead.model_validate(group)


async def get_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> GroupRead:
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

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
    user_id: int,
    group_id: int,
    group_update: GroupUpdate | GroupUpdatePartial,
    partial: bool = False,
) -> GroupRead:
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
) -> Sequence[UserRead]:
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement = select(User).join(Account).where(Account.group_id == group_id)

    result = await session.execute(statement)
    users = list(result.scalars().all())

    return [UserRead.model_validate(user) for user in users]


async def get_assignments_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[AssignmentRead]:
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
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    return {"link": f"http://oriole.com/join/{group_id}"}
