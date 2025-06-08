from typing import Sequence

from sqlalchemy import select, func, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import Account, Group
from features.groups.schemas import AccountRole, AccountReadPartial, GroupReadPartial
from features.groups.schemas import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)
from features.groups.validators import (
    get_group_if_exists,
    check_owner_permission_in_group,
    check_user_in_group,
)
from features.modules.models import Module
from features.modules.schemas import ModuleReadPartial
from features.tasks.models import Task, UserReply
from features.users.models import UserProfile
from features.users.schemas import UserProfileRead
from features.users.validators import check_user_exists


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
        modules=[],
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

    statement_modules = (
        select(
            Module,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.module_id == Module.id)
        .where(Module.group_id == group_id)
        .group_by(Module.id)
        .order_by(Module.id)
    )
    result_modules: Result = await session.execute(statement_modules)
    modules = result_modules.all()

    group_modules = []
    for module, tasks_count in modules:
        tasks_query = await session.execute(
            select(Task).where(Task.module_id == module.id)
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

        group_modules.append(
            ModuleReadPartial(
                id=module.id,
                title=module.title,
                description=module.description,
                is_contest=module.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
                is_active=module.is_active,
            )
        )

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[
            AccountReadPartial.model_validate(account.__dict__) for account in accounts
        ],
        modules=group_modules,
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

    statement_modules = (
        select(
            Module,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.module_id == Module.id)
        .where(Module.group_id == group_id)
        .group_by(Module.id)
        .order_by(Module.id)
    )
    result_modules: Result = await session.execute(statement_modules)
    modules = result_modules.all()

    group_modules = []
    for module, tasks_count in modules:
        tasks_query = await session.execute(
            select(Task).where(Task.module_id == module.id)
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

        group_modules.append(
            ModuleReadPartial(
                id=module.id,
                title=module.title,
                description=module.description,
                is_contest=module.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
                is_active=module.is_active,
            )
        )

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[
            AccountReadPartial.model_validate(account.__dict__) for account in accounts
        ],
        modules=group_modules,
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

    await session.execute(
        delete(UserReply).where(
            UserReply.task_id.in_(
                select(Task.id).where(
                    Task.module_id.in_(
                        select(Module.id).where(Module.group_id == group_id)
                    )
                )
            )
        )
    )

    await session.execute(
        delete(Task).where(
            Task.module_id.in_(select(Module.id).where(Module.group_id == group_id))
        )
    )

    await session.execute(delete(Module).where(Module.group_id == group_id))
    await delete_group_invites(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
    await session.execute(delete(Account).where(Account.group_id == group_id))

    await session.delete(group)
    await session.commit()
