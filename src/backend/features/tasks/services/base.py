from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.modules.crud.module as module_crud
import features.solutions.crud.base as solution_crud
import features.tasks.crud.base as task_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.validators import get_module_or_404
from features.tasks.schemas import BaseTaskRead
from features.tasks.validators import get_task_or_404


async def get_task_by_id(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    include: list[str] | None = None,
) -> BaseTaskRead:
    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    solutions = []
    if include and "solutions" in include:
        solutions = await solution_crud.get_solutions_by_account_id_and_task_id(
            session, account.id, task_id
        )
# TODO: change to real solution object
    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions)

    return task.get_validation_schema(
        is_correct=is_correct, user_attempts=user_attempts
    )


async def get_tasks_in_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    is_active: bool | None,
) -> list[BaseTaskRead]:
    module = await get_module_or_404(session, module_id)
    await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    tasks = await task_crud.get_tasks_by_module_id(session, module_id, is_active)
    if not tasks:
        return []

    solutions = await solution_crud.get_solutions_by_account_id_and_task_ids(
        session, account.id, [task.id for task in tasks]
    )

    return mapper.build_base_task_reads_list(tasks, solutions)


async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
    is_active: bool | None,
) -> list[BaseTaskRead]:
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

    solutions = await solution_crud.get_solutions_by_account_ids_and_task_ids(
        session,
        [account.id for account in accounts],
        task_ids=[task.id for task in tasks],
    )

    return mapper.build_base_task_reads_list(tasks, solutions)


async def delete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> None:
    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    await solution_crud.delete_solutions_by_task_id(session, task_id)
    await task_crud.delete_task(session, task)
