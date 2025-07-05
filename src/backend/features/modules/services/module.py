from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.modules.crud.module as module_crud
import features.modules.mappers as mapper
import features.solutions.crud.base as solution_crud
import features.tasks.crud.base as task_crud
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.schemas import (
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
)
from features.modules.schemas.module import (
    ModuleReadWithPerformance,
    ModuleReadWithTasks,
)
from features.modules.validators import get_module_or_404
from features.spaces.validators import get_space_or_404
from shared.validators import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
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

    module = await module_crud.create_module(session, module_in, user_id)
    return module.get_validation_schema()


async def get_module_by_id(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    include: list[str] | None = None,
) -> ModuleReadWithPerformance | ModuleReadWithTasks:
    module = await get_module_or_404(session, module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)
    tasks = await task_crud.get_tasks_by_module_id(session, module_id)
    solutions = await solution_crud.get_solutions_by_account_id_and_task_ids(
        session, account.id, [task.id for task in tasks]
    )
    if include and "tasks" in include:
        return mapper.build_module_read_with_tasks(module, tasks, solutions)
    return mapper.build_module_read_with_performance(module, tasks, solutions)


async def get_modules_in_space(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    is_active: bool | None = None,
) -> list[ModuleRead]:
    _ = await get_group_or_404(session, space_id)
    account = await get_account_or_404(session, user_id, space_id)

    modules = await module_crud.get_modules_by_space_ids(session, [space_id], is_active)
    if not modules:
        return []

    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module in modules]
    )
    solutions = await solution_crud.get_solutions_by_account_id_and_task_ids(
        session, account.id, [task.id for task in tasks]
    )
    return mapper.build_module_read_with_performance_list(modules, tasks, solutions)


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

    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module in modules]
    )
    solutions = await solution_crud.get_solutions_by_account_ids_and_task_ids(
        session, account_ids, [task.id for task in tasks]
    )
    return mapper.build_module_read_with_performance_list(modules, tasks, solutions)


async def update_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    module_update: ModuleUpdate,
) -> ModuleRead:
    module = await get_module_or_404(session, module_id)
    _ = await get_group_or_404(session, module.space_id)
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
    tasks = await task_crud.get_tasks_by_module_id(session, module.id)
    solutions = await solution_crud.get_solutions_by_account_id_and_task_ids(
        session, account.id, [task.id for task in tasks]
    )
    return mapper.build_module_read_with_performance(module, tasks, solutions)


async def delete_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
) -> None:
    module = await get_module_or_404(session=session, module_id=module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    tasks = await task_crud.get_tasks_by_module_id(session, module_id)

    for task in tasks:
        await solution_crud.delete_solutions_by_task_id(session, task.id)
        await task_crud.delete_task(session, task)

    await module_crud.delete_module(session, module)
