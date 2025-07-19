from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.groups.crud.group_invite as group_invite_crud
import features.groups.mappers as mapper
import features.modules.crud.module as module_crud
import features.solutions.crud.base as solutions_crud
import features.tasks.crud.base as task_crud
import features.users.crud.user_profile as user_profile_crud
from features.accounts.schemas import AccountRole
from features.groups.schemas import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
)
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
    check_user_is_owner,
)
from shared.enums import SpaceTypeEnum


async def create_group(
    session: AsyncSession,
    user_id: int,
    group_in: GroupCreate,
) -> GroupRead:
    group = await group_crud.create_group(session, group_in, user_id)
    _ = await account_crud.create_account(
        session, user_id, group.id, AccountRole.OWNER.value
    )

    return group.get_validation_schema()


async def get_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    include: list[str] | None = None,
) -> GroupRead:
    group = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    accounts = await account_crud.get_accounts_in_space(session, group_id)
    user_profiles = await user_profile_crud.get_user_profiles_by_user_ids(
        session, [account.user_id for account in accounts]
    )
    modules = await module_crud.get_modules_by_group_id(session, group_id)
    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module in modules]
    )
    solutions = await solutions_crud.get_solutions_by_account_id_and_task_ids(
        session, account.id, [task.id for task in tasks]
    )

    if include:
        if "accounts" in include and "modules" in include:
            return mapper.build_group_read_with_accounts_and_modules(
                group, accounts, user_profiles, modules, tasks, solutions
            )
        elif "accounts" in include:
            return mapper.build_group_read_with_accounts(group, accounts, user_profiles)
        elif "modules" in include:
            return mapper.build_group_read_with_modules(
                group, modules, tasks, solutions
            )
    return group.get_validation_schema()


async def get_user_groups(
    session: AsyncSession,
    user_id: int,
) -> list[GroupRead]:
    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    space_ids = [account.space_id for account in accounts]
    spaces = await group_crud.get_groups_by_ids(session, space_ids)
    groups = [g for g in spaces if g.space_type == SpaceTypeEnum.GROUP]

    return mapper.build_group_read_list(groups)


async def update_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    group_update: GroupUpdate,
) -> GroupRead:
    group = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    check_user_is_owner(account.role)

    update_data = group_update.model_dump(exclude_unset=True)
    group = await group_crud.update_group(session, group, update_data)

    return group.get_validation_schema()


async def delete_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    group = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    check_user_is_admin_or_owner(account.role)

    modules = await module_crud.get_modules_by_group_id(session, group_id)

    for module in modules:
        tasks = await task_crud.get_tasks_by_module_id(session, module.id)

        for task in tasks:
            await solutions_crud.delete_solutions_by_task_id(session, task.id)
            await task_crud.delete_task(session, task)

        await module_crud.delete_module(session, module)

    await group_invite_crud.delete_group_invites_by_group_id(session, group_id)
    await account_crud.delete_accounts_by_space_id(session, group_id)

    await group_crud.delete_group(session, group)
