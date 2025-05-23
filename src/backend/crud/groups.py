from datetime import datetime, timedelta
from typing import Sequence
from fastapi import Request
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import urljoin

from core.models.group_invite import GroupInvite
from exceptions.user import check_user_exists

from exceptions.group import (
    get_group_if_exists,
    check_admin_permission_in_group,
    check_owner_permission_in_group,
    check_user_in_group,
    check_user_is_member,
    validate_invite_code,
)

from core.schemas.user import UserProfileRead
from core.schemas.account import AccountRole, AccountReadPartial
from core.schemas.assignment import AssignmentReadPartial

from core.schemas.group import (
    GroupCreate,
    GroupRead,
    GroupReadPartial,
    GroupUpdate,
    GroupUpdatePartial,
)
from core.models import (
    Account,
    Assignment,
    Group,
    UserProfile,
    Task,
    UserReply,
)
from utils.code_generator import generate_alphanum_code


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

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[AccountReadPartial.model_validate(admin_account.__dict__)],
        assignments=[],
    )


async def get_group_by_id(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> GroupRead:
    await check_user_exists(session=session, user_id=user_id)
    group = await get_group_if_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement_accounts = select(Account).where(Account.group_id == group_id)
    result_accounts: Result = await session.execute(statement_accounts)
    accounts = result_accounts.scalars().all()

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    statement_assignments = (
        select(
            Assignment,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.assignment_id == Assignment.id)
        .where(Assignment.group_id == group_id)
        .group_by(Assignment.id)
        .order_by(Assignment.id)
    )
    result_assignments: Result = await session.execute(statement_assignments)
    assignments = result_assignments.all()

    group_assignments = []
    for assignment, tasks_count in assignments:
        tasks_query = await session.execute(
            select(Task).where(Task.assignment_id == assignment.id)
        )
        tasks = tasks_query.scalars().all()

        user_reply_data = await session.execute(
            select(UserReply).where(
                UserReply.account_id == account.id,
                UserReply.task_id.in_([task.id for task in tasks]),
            )
        )

        user_replies = {
            reply.task_id: reply for reply in user_reply_data.scalars().all()
        }

        user_completed_tasks_count = sum(
            1 for reply in user_replies.values() if reply.is_correct
        )

        group_assignments.append(
            AssignmentReadPartial(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                is_contest=assignment.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
                is_active=assignment.is_active,
            )
        )

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[
            AccountReadPartial.model_validate(account.__dict__) for account in accounts
        ],
        assignments=group_assignments,
    )


async def get_user_groups(
    session: AsyncSession,
    user_id: int,
) -> Sequence[GroupReadPartial]:
    await check_user_exists(session=session, user_id=user_id)

    statement = (
        select(Group).join(Account).where(Account.user_id == user_id).order_by(Group.id)
    )

    result: Result = await session.execute(statement)
    groups = list(result.scalars().all())

    return [GroupReadPartial.model_validate(group) for group in groups]


async def update_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    group_update: GroupUpdate | GroupUpdatePartial,
    is_partial: bool = False,
) -> GroupRead:
    await check_user_exists(session=session, user_id=user_id)
    group = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)
    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    for key, value in group_update.model_dump(exclude_unset=is_partial).items():
        setattr(group, key, value)

    await session.commit()
    await session.refresh(group)

    statement_accounts = select(Account).where(Account.group_id == group_id)
    result_accounts: Result = await session.execute(statement_accounts)
    accounts = result_accounts.scalars().all()

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    statement_assignments = (
        select(
            Assignment,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.assignment_id == Assignment.id)
        .where(Assignment.group_id == group_id)
        .group_by(Assignment.id)
        .order_by(Assignment.id)
    )
    result_assignments: Result = await session.execute(statement_assignments)
    assignments = result_assignments.all()

    group_assignments = []
    for assignment, tasks_count in assignments:
        tasks_query = await session.execute(
            select(Task).where(Task.assignment_id == assignment.id)
        )
        tasks = tasks_query.scalars().all()

        user_reply_data = await session.execute(
            select(UserReply).where(
                UserReply.account_id == account.id,
                UserReply.task_id.in_([task.id for task in tasks]),
            )
        )

        user_replies = {
            reply.task_id: reply for reply in user_reply_data.scalars().all()
        }

        user_completed_tasks_count = sum(
            1 for reply in user_replies.values() if reply.is_correct
        )

        group_assignments.append(
            AssignmentReadPartial(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                is_contest=assignment.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
                is_active=assignment.is_active,
            )
        )

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[
            AccountReadPartial.model_validate(account.__dict__) for account in accounts
        ],
        assignments=group_assignments,
    )


async def delete_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    group = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)
    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(Account.group_id == group_id)
    result: Result = await session.execute(statement)
    accounts_to_delete = result.scalars().all()

    for account in accounts_to_delete:
        await session.delete(account)

    await session.delete(group)
    await session.commit()


async def get_users_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[UserProfileRead]:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement_accounts = select(Account).where(Account.group_id == group_id)
    result_accounts: Result = await session.execute(statement_accounts)
    accounts = result_accounts.scalars().all()

    user_profiles = []
    for account in accounts:
        user_profile = await session.get(UserProfile, account.user_id)
        if user_profile:
            user_profiles.append(user_profile)

    return [
        UserProfileRead.model_validate(user_profile) for user_profile in user_profiles
    ]


async def get_assignments_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[AssignmentReadPartial]:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement = (
        select(
            Assignment,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.assignment_id == Assignment.id)
        .where(Assignment.group_id == group_id)
        .group_by(Assignment.id)
        .order_by(Assignment.id)
    )

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    if not account:
        return []

    result: Result = await session.execute(statement)
    assignments = result.all()

    assignment_results = []
    for assignment, tasks_count in assignments:

        tasks_query = await session.execute(
            select(Task).where(Task.assignment_id == assignment.id)
        )
        tasks = tasks_query.scalars().all()

        user_reply_data = await session.execute(
            select(UserReply).where(
                UserReply.account_id == account.id,
                UserReply.task_id.in_([task.id for task in tasks]),
            )
        )

        user_replies = {
            reply.task_id: reply for reply in user_reply_data.scalars().all()
        }

        user_completed_tasks_count = sum(
            1 for reply in user_replies.values() if reply.is_correct
        )

        assignment_results.append(
            AssignmentReadPartial(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                is_contest=assignment.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
                is_active=assignment.is_active,
            )
        )

    return assignment_results


async def invite_user(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_id: int,
    expires_minutes: int,
) -> dict:
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )

    code = generate_alphanum_code()

    invite = GroupInvite(
        code=code,
        group_id=group_id,
        expires_at=datetime.now() + timedelta(minutes=expires_minutes),
        is_active=True,
    )

    session.add(invite)
    await session.commit()

    base_url = str(request.base_url)
    base_url = base_url[:-1] if base_url.endswith("/") else base_url

    return {"link": urljoin(base_url, f"api/v1/learn/groups/join/{code}")}


async def join_by_link(
    session: AsyncSession,
    user_id: int,
    invite_code: str,
) -> str:

    await check_user_exists(session=session, user_id=user_id)

    invite = await validate_invite_code(session, invite_code)
    group_id = invite.group_id

    await check_user_in_group(session, user_id, group_id, is_correct=False)

    existing_accounts = await session.execute(
        select(Account).where(Account.group_id == group_id)
    )
    role = (
        AccountRole.OWNER
        if not existing_accounts.scalars().all()
        else AccountRole.MEMBER
    )

    account = Account(user_id=user_id, group_id=group_id, role=role.value)
    invite.is_active = False
    session.add(account)
    await session.commit()

    return "success"


async def promote_user_to_admin(
    session: AsyncSession,
    user_id: int,
    promote_user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=promote_user_id)

    _ = await get_group_if_exists(session=session, group_id=group_id)

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
    result: Result = await session.execute(statement)
    account = result.scalars().first()

    await check_user_is_member(role=account.role, user_id=user_id)

    account.role = AccountRole.ADMIN

    await session.commit()


async def demote_user_to_member(
    session: AsyncSession,
    user_id: int,
    demote_user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=demote_user_id)

    _ = await get_group_if_exists(session=session, group_id=group_id)

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
    result: Result = await session.execute(statement)
    account = result.scalars().first()

    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    account.role = AccountRole.MEMBER

    await session.commit()


async def remove_user_from_group(
    session: AsyncSession,
    user_id: int,
    remove_user_id: int,
    group_id: int,
) -> None:
    if user_id == remove_user_id:
        await leave_from_group(session=session, user_id=user_id, group_id=group_id)
        return

    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=remove_user_id)

    _ = await get_group_if_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=remove_user_id
    )

    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(
        Account.user_id == remove_user_id, Account.group_id == group_id
    )
    result: Result = await session.execute(statement)
    account = result.scalars().first()

    await session.delete(account)
    await session.commit()


async def leave_from_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    account = await session.execute(
        select(Account).where(Account.user_id == user_id, Account.group_id == group_id)
    )
    account = account.scalars().first()

    if account.role == AccountRole.OWNER.value:
        admins = await session.execute(
            select(Account).where(
                Account.group_id == group_id, Account.role == AccountRole.ADMIN.value
            )
        )
        admin_accounts = admins.scalars().all()

        if admin_accounts:
            new_owner = min(admin_accounts, key=lambda a: a.user_id)
            new_owner.role = AccountRole.OWNER.value
            account.role = AccountRole.MEMBER.value
        else:
            members = await session.execute(
                select(Account).where(
                    Account.group_id == group_id, Account.role == "member"
                )
            )
            member_accounts = members.scalars().all()

            if member_accounts:
                new_owner = min(member_accounts, key=lambda a: a.user__id)
                new_owner.role = AccountRole.OWNER.value
                account.role = AccountRole.MEMBER.value

    await session.delete(account)
    await session.commit()
