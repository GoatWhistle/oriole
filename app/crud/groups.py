from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_owner_permission_in_group,
    check_user_in_group,
    check_user_is_member,
)

from core.exceptions.user import check_user_exists

from core.schemas.account import AccountRole, AccountRead

from core.schemas.assignment import AssignmentRead

from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
    GroupDataRead,
)

from core.models import (
    Account,
    Assignment,
    Group,
    User,
    UserProfile,
)


async def create_group(
    session: AsyncSession,
    user_id: int,
    group_in: GroupCreate,
) -> GroupRead:

    await check_user_exists(session=session, user_id=user_id)

    group = Group(**group_in.model_dump())

    session.add(group)
    await session.commit()
    await session.refresh(group)

    admin_account = Account(
        user_id=user_id,
        group_id=group.id,
        role=AccountRole.OWNER.value,
    )
    session.add(admin_account)
    await session.commit()

    return GroupRead.model_validate(group)


# TODO: TEST
async def get_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> GroupDataRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    group = await session.get(Group, group_id)

    statement_accounts = select(Account).where(Account.group_id == group_id)
    result_accounts = await session.execute(statement_accounts)
    accounts = result_accounts.scalars().all()

    statement_assignments = select(Assignment).where(Assignment.group_id == group_id)
    result_assignments: Result = await session.execute(statement_assignments)
    assignments = result_assignments.scalars().all()

    return GroupDataRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[AccountRead.model_validate(account.__dict__) for account in accounts],
        assignments=[
            AssignmentRead.model_validate(assignment.__dict__)
            for assignment in assignments
        ],
    )


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
    await check_owner_permission_in_group(
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
    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    group = await session.get(Group, group_id)

    statement = select(Account).where(Account.group_id == group_id)
    result = await session.execute(statement)
    accounts_to_delete = result.scalars().all()

    for account in accounts_to_delete:
        await session.delete(account)

    await session.delete(group)
    await session.commit()


# TODO: TEST
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


async def invite_user(
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

    return {"link": f"http://oriole.com/learn/groups/join/{group_id}"}


# TODO: TEST
async def join_by_link(
    session: AsyncSession,
    user_id: int,
    group_id: int,
):
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
        is_correct=False,
    )

    new_account = Account(
        user_id=user_id,
        group_id=group_id,
        role=AccountRole.MEMBER.value,
    )

    session.add(new_account)
    await session.commit()

    return await get_group(session=session, user_id=user_id, group_id=group_id)


# TODO: TEST
async def promote_user_to_admin(
    session: AsyncSession,
    user_id: int,
    promote_user_id: int,
    group_id: int,
):
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=promote_user_id)

    await check_group_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=promote_user_id
    )

    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(
        Account.user_id == promote_user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    await check_user_is_member(role=account.role, user_id=user_id)

    account.role = AccountRole.ADMIN

    await session.commit()

    return {"detail": f"User {user_id} has been promoted to ADMIN in group {group_id}."}


# TODO: TEST
async def demote_user_to_member(
    session: AsyncSession,
    user_id: int,
    demote_user_id: int,
    group_id: int,
):
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=demote_user_id)

    await check_group_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=demote_user_id
    )

    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(
        Account.user_id == demote_user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    account.role = AccountRole.MEMBER

    await session.commit()

    return {"detail": f"User {user_id} has been demoted to MEMBER in group {group_id}."}


# TODO: TEST
async def remove_user_from_group(
    session: AsyncSession,
    user_id: int,
    remove_user_id: int,
    group_id: int,
):
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=remove_user_id)

    await check_group_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=remove_user_id
    )

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    await session.delete(account)
    await session.commit()

    return {"detail": f"User {user_id} has been removed from group {group_id}."}
