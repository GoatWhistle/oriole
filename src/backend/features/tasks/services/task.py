from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.account as account_crud
import features.modules.crud.module as module_crud
import features.tasks.crud.task as task_crud
import features.tasks.crud.user_reply as user_reply_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.validators import get_module_or_404
from features.tasks.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
)
from features.tasks.schemas.task import TaskReadWithoutReplies
from features.tasks.validators import (
    get_task_or_404,
    check_task_start_deadline_after_module_start,
    check_task_end_deadline_before_module_end,
)
from features.users.validators import check_user_exists
from shared.validators import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
)


async def create_task(
    session: AsyncSession,
    user_id: int,
    task_in: TaskCreate,
) -> TaskRead:
    await check_user_exists(session, user_id)

    module = await get_module_or_404(session, task_in.module_id)
    _ = await get_group_or_404(session, module.group_id)
    account = await get_account_or_404(session, user_id, module.group_id)

    check_user_is_admin_or_owner(account.role)

    check_start_time_not_in_past(task_in.start_datetime)
    check_end_time_not_in_past(task_in.end_datetime)
    check_end_time_is_after_start_time(task_in.start_datetime, task_in.end_datetime)
    check_task_start_deadline_after_module_start(
        task_in.start_datetime, module.start_datetime
    )
    check_task_end_deadline_before_module_end(task_in.end_datetime, module.end_datetime)

    task = await task_crud.create_task(session, task_in)
    await module_crud.increment_module_tasks_count(session, module.id)

    return mapper.build_task_read(task, module)


async def get_task_by_id(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    include: list[str] | None,
) -> TaskRead | TaskReadWithoutReplies:
    await check_user_exists(session, user_id)

    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.group_id)
    account = await get_account_or_404(session, user_id, module.group_id)
    user_reply = (
        await user_reply_crud.get_user_reply_by_account_id_and_task_id(
            session, account.id, task_id
        )
        if include and "user_replies" in include
        else []
    )

    return mapper.build_task_read(task, module, user_reply)


async def get_tasks_in_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    is_active: bool | None,
    include: list[str] | None,
) -> list[TaskRead]:
    await check_user_exists(session, user_id)

    module = await get_module_or_404(session, module_id)
    _ = await get_group_or_404(session, module.group_id)
    account = await get_account_or_404(session, user_id, module.group_id)

    tasks = await task_crud.get_tasks_by_module_id(session, module_id, is_active)
    if not tasks:
        return []

    user_replies = (
        await user_reply_crud.get_user_replies_by_account_ids_and_task_ids(
            session, [account.id], [task.id for task in tasks]
        )
        if include and "user_replies" in include
        else []
    )

    return mapper.build_task_read_list([module], tasks, user_replies)


async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
    is_active: bool | None,
    include: list[str] | None,
) -> list[TaskRead | TaskReadWithoutReplies]:
    await check_user_exists(session=session, user_id=user_id)

    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    modules = await module_crud.get_modules_by_group_ids(
        session, [account.group_id for account in accounts], is_active
    )
    if not modules:
        return []

    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module in modules], is_active
    )
    if not tasks:
        return []

    user_replies = (
        await user_reply_crud.get_user_replies_by_account_ids_and_task_ids(
            session, [account.id for account in accounts], [task.id for task in tasks]
        )
        if include and "user_replies" in include
        else []
    )

    return mapper.build_task_read_list(modules, tasks, user_replies)


async def update_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: TaskUpdate | TaskUpdatePartial,
    is_partial: bool = False,
) -> TaskRead:
    await check_user_exists(session, user_id)

    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.group_id)
    account = await get_account_or_404(session, user_id, module.group_id)

    check_user_is_admin_or_owner(account.role)

    update_data = task_update.model_dump(exclude_unset=is_partial)

    if "start_datetime" in update_data:
        check_start_time_not_in_past(update_data["start_datetime"])
    if "end_datetime" in update_data:
        check_end_time_not_in_past(update_data["end_datetime"])

    if "start_datetime" in update_data or "end_datetime" in update_data:
        start = update_data.get("start_datetime", task.start_datetime)
        end = update_data.get("end_datetime", task.end_datetime)
        check_end_time_is_after_start_time(start, end)

    check_task_start_deadline_after_module_start(
        task.start_datetime, module.start_datetime
    )
    check_task_end_deadline_before_module_end(task.end_datetime, module.end_datetime)

    task = await task_crud.update_task(session, task, update_data)

    return mapper.build_task_read(task, module)


async def delete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> None:
    await check_user_exists(session, user_id)

    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.group_id)
    account = await get_account_or_404(session, user_id, module.group_id)

    check_user_is_admin_or_owner(account.role)

    await user_reply_crud.delete_user_replies_by_task_id(session, task_id)
    await task_crud.delete_task(session, task)
