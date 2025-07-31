from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.modules.crud.account_module_progress as module_progress_crud
import features.modules.crud.module as module_crud
import features.modules.mappers as mapper
import features.solutions.crud.base as solution_crud
import features.tasks.crud.account_task_progress as task_progress_crud
import features.tasks.crud.base as task_crud
from features.groups.validators import check_user_is_admin_or_owner, get_account_or_404
from features.modules.schemas import ModuleCreate, ModuleRead, ModuleUpdate
from features.modules.schemas.module import (
    ModuleReadWithProgress,
    ModuleReadWithTasks,
)
from features.modules.validators import get_module_or_404
from features.spaces.validators import get_space_or_404
from shared.validators import (
    check_end_time_is_after_start_time,
    check_end_time_not_in_past,
    check_start_time_not_in_past,
)


async def create_module(
    session: AsyncSession,
    user_id: int,
    module_in: ModuleCreate,
) -> ModuleRead:
    _ = await get_space_or_404(session, module_in.space_id)
    account = await get_account_or_404(session, user_id, module_in.space_id)

    check_user_is_admin_or_owner(account.role)

    check_start_time_not_in_past(module_in.start_datetime)
    check_end_time_not_in_past(module_in.end_datetime)
    check_end_time_is_after_start_time(module_in.start_datetime, module_in.end_datetime)

    module = await module_crud.create_module(session, module_in, account.id)

    return mapper.build_module_read_with_progress(module)


async def get_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    include: list[str] | None = None,
) -> ModuleReadWithProgress | ModuleReadWithTasks:
    module = await get_module_or_404(session, module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    account_module_progress = await module_progress_crud.get_account_module_progress_by_account_id_and_module_id(
        session, account.id, module_id
    )
    if include and "tasks" in include:
        tasks = await task_crud.get_tasks_by_module_id(session, module_id)
        account_task_progresses = await task_progress_crud.get_account_task_progresses_by_account_id_and_task_ids(
            session, account.id, [task.id for task in tasks]
        )

        return mapper.build_module_read_with_tasks(
            module, account_module_progress, tasks, account_task_progresses
        )

    return mapper.build_module_read_with_progress(module, account_module_progress)


async def get_modules_in_space(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    is_active: bool | None = None,
) -> list[ModuleRead]:
    _ = await get_space_or_404(session, space_id)
    account = await get_account_or_404(session, user_id, space_id)

    modules = await module_crud.get_modules_by_space_ids(session, [space_id], is_active)
    if not modules:
        return []

    account_module_progress = await module_progress_crud.get_account_module_progresses_by_account_id_and_module_ids(
        session, account.id, [module.id for module in modules]
    )

    return mapper.build_module_read_with_progress_list(modules, account_module_progress)


async def get_user_modules(
    session: AsyncSession,
    user_id: int,
    is_active: bool | None = None,
) -> list[ModuleRead]:
    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    account_ids = [account.id for account in accounts]

    groups = await group_crud.get_groups_by_account_ids(session, account_ids)
    if not groups:
        return []

    modules = await module_crud.get_modules_by_space_ids(
        session, [group.id for group in groups], is_active
    )
    if not modules:
        return []

    account_module_progress = await module_progress_crud.get_account_module_progresses_by_account_ids_and_module_ids(
        session, [account.id for account in accounts], [module.id for module in modules]
    )

    return mapper.build_module_read_with_progress_list(modules, account_module_progress)


async def update_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    module_update: ModuleUpdate,
) -> ModuleRead:
    module = await get_module_or_404(session, module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = module_update.model_dump(exclude_unset=True)

    if "start_datetime" in update_data:
        check_start_time_not_in_past(update_data["start_datetime"])
    if "end_datetime" in update_data:
        check_end_time_not_in_past(update_data["end_datetime"])

    if "start_datetime" in update_data or "end_datetime" in update_data:
        start = update_data.get("start_datetime", module.start_datetime)
        end = update_data.get("end_datetime", module.end_datetime)
        check_end_time_is_after_start_time(start, end)

    module = await module_crud.update_module(session, module, update_data)
    account_module_progress = await module_progress_crud.get_account_module_progress_by_account_id_and_module_id(
        session, account.id, module_id
    )
    return mapper.build_module_read_with_progress(module, account_module_progress)


async def delete_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
) -> None:
    module = await get_module_or_404(session=session, module_id=module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    tasks = await task_crud.get_tasks_by_module_id(session, module_id)

    for task in tasks:
        await solution_crud.delete_solutions_by_task_id(session, task.id)
        await task_progress_crud.delete_account_task_progresses_by_task_id(
            session, task.id
        )
        await task_crud.delete_task(session, task)
    await module_progress_crud.delete_account_module_progresses_by_module_id(
        session, module_id
    )
    await module_crud.delete_module(session, module)
