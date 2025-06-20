from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.modules.crud.module as module_crud
import features.modules.mappers as mapper
import features.tasks.crud.task as task_crud
import features.tasks.crud.user_reply as user_reply_crud
from features.groups.validators import (
    get_group_if_exists,
    get_account_if_exists,
    check_user_is_admin_or_owner,
)
from features.modules.schemas import (
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
    ModuleUpdatePartial,
    ModuleReadPartial,
)
from features.modules.validators import get_module_if_exists
from features.tasks.models import Task
from features.users.validators import check_user_exists
from validators import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
)


async def create_module(
    session: AsyncSession,
    user_id: int,
    module_in: ModuleCreate,
) -> ModuleRead:
    await check_user_exists(session, user_id)

    _ = await get_group_if_exists(session, module_in.group_id)
    account = await get_account_if_exists(session, user_id, module_in.group_id)

    check_user_is_admin_or_owner(account.role, user_id)

    check_start_time_not_in_past(module_in.start_datetime, obj_name="module")
    check_end_time_not_in_past(module_in.end_datetime, obj_name="module")
    check_end_time_is_after_start_time(
        module_in.start_datetime, module_in.end_datetime, obj_name="module"
    )

    module = await module_crud.create_module(session, module_in, user_id)

    return mapper.build_module_read(module, module_in.group_id)


async def get_module_by_id(
    session: AsyncSession,
    user_id: int,
    module_id: int,
) -> ModuleRead:
    await check_user_exists(session, user_id)

    module, tasks_count = await module_crud.get_module_with_task_count(
        session, module_id
    )
    _ = await get_group_if_exists(session, module.group_id)
    account = await get_account_if_exists(session, user_id, module.group_id)
    tasks = await task_crud.get_tasks_by_module_id(session, module_id)
    user_replies = await user_reply_crud.get_user_replies_by_task_ids(
        session, account.id, [task.id for task in tasks]
    )

    return mapper.build_module_read(module, module.group_id, tasks, user_replies)


async def get_modules_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    is_active: bool | None = None,
) -> Sequence[ModuleReadPartial]:
    await check_user_exists(session, user_id)

    _ = await get_group_if_exists(session, group_id)
    account = await get_account_if_exists(session, user_id, group_id)

    modules_with_counts = await module_crud.get_modules_by_group_ids_with_task_counts(
        session, [group_id], is_active
    )
    if not modules_with_counts:
        return []

    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module, _ in modules_with_counts]
    )
    tasks_by_module_id: dict[int, list[Task]] = {}
    for task in tasks:
        tasks_by_module_id.setdefault(task.module_id, []).append(task)

    user_replies = await user_reply_crud.get_user_replies_by_account_ids_and_task_ids(
        session, [account.id], [task.id for task in tasks]
    )
    replies_by_task_id = {reply.task_id: reply for reply in user_replies}

    return mapper.build_module_read_partial_list(
        modules_with_counts,
        tasks_by_module_id,
        replies_by_task_id,
    )


async def get_user_modules(
    session: AsyncSession, user_id: int, is_active: bool | None = None
) -> Sequence[ModuleReadPartial]:
    await check_user_exists(session=session, user_id=user_id)

    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    account_ids = [account.id for account in accounts]

    groups = await group_crud.get_groups_by_account_ids(session, account_ids)
    if not groups:
        return []

    modules_with_counts = await module_crud.get_modules_by_group_ids_with_task_counts(
        session, [group.id for group in groups], is_active
    )
    if not modules_with_counts:
        return []

    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module, _ in modules_with_counts]
    )
    tasks_by_module_id: dict[int, list[Task]] = {}
    for task in tasks:
        tasks_by_module_id.setdefault(task.module_id, []).append(task)

    user_replies = await user_reply_crud.get_user_replies_by_account_ids_and_task_ids(
        session,
        account_ids,
        [task.id for task in tasks],
    )
    replies_by_task_id = {reply.task_id: reply for reply in user_replies}

    return mapper.build_module_read_partial_list(
        modules_with_counts, tasks_by_module_id, replies_by_task_id
    )


async def update_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    module_update: ModuleUpdate | ModuleUpdatePartial,
    is_partial: bool = False,
) -> ModuleRead:
    await check_user_exists(session, user_id)

    module = await get_module_if_exists(session, module_id)
    _ = await get_group_if_exists(session, module.group_id)
    account = await get_account_if_exists(session, user_id, module.group_id)

    check_user_is_admin_or_owner(account.role, user_id)

    update_data = module_update.model_dump(exclude_unset=is_partial)

    if "start_datetime" in update_data:
        check_start_time_not_in_past(update_data["start_datetime"], obj=module)
    if "end_datetime" in update_data:
        check_end_time_not_in_past(update_data["end_datetime"], obj=module)

    if "start_datetime" in update_data or "end_datetime" in update_data:
        start = update_data.get("start_datetime", module.start_datetime)
        end = update_data.get("end_datetime", module.end_datetime)
        check_end_time_is_after_start_time(start, end, obj=module)

    module = await module_crud.update_module(session, module, update_data)
    tasks = await task_crud.get_tasks_by_module_id(session, module.id)

    user_replies = await user_reply_crud.get_user_replies_by_task_ids(
        session, account.id, [task.id for task in tasks]
    )

    return mapper.build_module_read(module, module.group_id, tasks, user_replies)


async def delete_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
) -> None:
    await check_user_exists(session, user_id)

    module = await get_module_if_exists(session=session, module_id=module_id)
    _ = await get_group_if_exists(session, module.group_id)
    account = await get_account_if_exists(session, user_id, module.group_id)

    check_user_is_admin_or_owner(account.role, user_id)

    tasks = await task_crud.get_tasks_by_module_id(session, module_id)

    for task in tasks:
        await user_reply_crud.delete_user_replies_by_task_id(session, task.id)
        await task_crud.delete_task(session, task)

    await module_crud.delete_module(session, module)
