from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.groups.crud.invite as group_invite_crud
import features.groups.mappers.group as mapper
import features.modules.crud.module as module_crud
import features.tasks.crud.task as task_crud
import features.tasks.crud.user_reply as user_reply_crud
import features.users.crud.user_profile as user_profile_crud
from features.groups.schemas import AccountRole, GroupReadPartial
from features.groups.schemas import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
    GroupUpdatePartial,
)
from features.groups.validators import (
    get_group_if_exists,
    get_account_if_exists,
    check_user_is_admin_or_owner,
    check_user_is_owner,
)
from features.users.schemas import UserProfileRead
from features.users.validators import check_user_exists


async def create_group(
    session: AsyncSession,
    user_id: int,
    group_in: GroupCreate,
) -> GroupRead:
    await check_user_exists(session, user_id)

    group = await group_crud.create_group(session, group_in)
    account = await account_crud.create_account(
        session, user_id, group.id, AccountRole.OWNER.value
    )

    return mapper.build_group_read(group, [account])


async def get_group_by_id(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> GroupRead:
    await check_user_exists(session, user_id)

    group = await get_group_if_exists(session, group_id)
    account = await get_account_if_exists(session, user_id, group_id)

    accounts = await account_crud.get_accounts_in_group(session, group_id)
    modules = await module_crud.get_modules_by_group_id_with_task_counts(
        session, group_id
    )

    task_map = {}
    all_task_ids = []

    for module, _ in modules:
        tasks = await task_crud.get_tasks_by_module_id(session, module.id)
        task_map[module.id] = tasks
        all_task_ids.extend(task.id for task in tasks)

    user_replies = await user_reply_crud.get_user_replies_by_task_ids(
        session, account.id, all_task_ids
    )

    return mapper.build_group_read(group, accounts, modules, task_map, user_replies)


async def get_user_groups(
    session: AsyncSession,
    user_id: int,
) -> Sequence[GroupReadPartial]:
    await check_user_exists(session=session, user_id=user_id)

    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    groups = await group_crud.get_groups_by_account_ids(
        session, [account.id for account in accounts]
    )

    return [GroupReadPartial.model_validate(group) for group in groups]


async def get_users_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[UserProfileRead]:
    await check_user_exists(session, user_id)

    _ = await get_group_if_exists(session, group_id)
    _ = await get_account_if_exists(session, user_id, group_id)

    accounts = await account_crud.get_accounts_by_group_id(session, group_id)
    user_profiles = await user_profile_crud.get_user_profiles_by_user_ids(
        session, [account.user_id for account in accounts]
    )

    return [UserProfileRead.model_validate(profile) for profile in user_profiles]


async def update_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    group_update: GroupUpdate | GroupUpdatePartial,
    is_partial: bool = False,
) -> GroupRead:
    await check_user_exists(session, user_id)

    group = await get_group_if_exists(session, group_id)
    account = await get_account_if_exists(session, user_id, group_id)

    check_user_is_owner(account.role, user_id)

    update_data = group_update.model_dump(exclude_unset=is_partial)
    group = await group_crud.update_group(session, group, update_data)

    accounts = await account_crud.get_accounts_in_group(session, group_id)
    modules = await module_crud.get_modules_by_group_id_with_task_counts(
        session, group_id
    )

    task_map = {}
    all_task_ids = []

    for module, _ in modules:
        tasks = await task_crud.get_tasks_by_module_id(session, module.id)
        task_map[module.id] = tasks
        all_task_ids.extend(task.id for task in tasks)

    user_replies = await user_reply_crud.get_user_replies_by_task_ids(
        session, account.id, all_task_ids
    )

    return mapper.build_group_read(group, accounts, modules, task_map, user_replies)


async def delete_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session, user_id)

    group = await get_group_if_exists(session, group_id)
    account = await get_account_if_exists(session, user_id, group_id)

    check_user_is_admin_or_owner(account.role, user_id)

    modules = await module_crud.get_modules_by_group_id(session, group_id)

    for module in modules:
        tasks = await task_crud.get_tasks_by_module_id(session, module.id)

        for task in tasks:
            await user_reply_crud.delete_user_replies_by_task_id(session, task.id)
            await task_crud.delete_task(session, task)

        await module_crud.delete_module(session, module)

    await group_invite_crud.delete_group_invites_by_group_id(session, group_id)
    await account_crud.delete_accounts_by_group_id(session, group_id)

    await group_crud.delete_group(session, group)
