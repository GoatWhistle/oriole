from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.modules.crud.module as module_crud
import features.solutions.crud.base as base_solution_crud
import features.tasks.crud.account_task_progress as progress_crud
import features.tasks.crud.base as base_task_crud
import features.tasks.mappers as mapper
from features.groups.validators import check_user_is_admin_or_owner, get_account_or_404
from features.modules.validators import get_module_or_404
from features.spaces.validators import get_space_or_404
from features.tasks.schemas import (
    BaseTaskReadWithProgress,
    BaseTaskReadWithSolutions,
)
from features.tasks.validators import get_task_or_404


async def get_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    include: list[str] | None = None,
) -> BaseTaskReadWithProgress | BaseTaskReadWithSolutions:
    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    account_task_progress = (
        await progress_crud.get_account_task_progress_by_account_id_and_task_id(
            session, account.id, task_id
        )
    )

    if include and "solutions" in include:
        solutions = await base_solution_crud.get_solutions_by_account_id_and_task_id(
            session, account.id, task_id
        )
        return mapper.build_base_task_read_with_solutions(
            task, solutions, account_task_progress
        )
    return mapper.build_base_task_read_with_progress(task, account_task_progress)


async def get_tasks_in_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    is_active: bool | None,
) -> list[BaseTaskReadWithProgress]:
    module = await get_module_or_404(session, module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    tasks = await base_task_crud.get_tasks_by_module_id(session, module_id, is_active)
    if not tasks:
        return []

    account_task_progresses = (
        await progress_crud.get_account_task_progresses_by_account_id_and_task_ids(
            session, account.id, [task.id for task in tasks]
        )
    )

    return mapper.build_base_task_read_with_progress_list(
        tasks, account_task_progresses
    )


async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
    is_active: bool | None,
) -> list[BaseTaskReadWithProgress]:
    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    modules = await module_crud.get_modules_by_space_ids(
        session, [account.space_id for account in accounts], is_active
    )
    if not modules:
        return []

    tasks = await base_task_crud.get_tasks_by_module_ids(
        session, [module.id for module in modules], is_active
    )
    if not tasks:
        return []

    account_task_progresses = (
        await progress_crud.get_account_task_progresses_by_account_ids_and_task_ids(
            session, [account.id for account in accounts], [task.id for task in tasks]
        )
    )

    return mapper.build_base_task_read_with_progress_list(
        tasks, account_task_progresses
    )


async def delete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> None:
    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    await base_solution_crud.delete_solutions_by_task_id(session, task_id)
    await progress_crud.delete_account_task_progresses_by_task_id(session, task_id)
    await base_task_crud.delete_task(session, task)
