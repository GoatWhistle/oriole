from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as solution_crud
import features.tasks.crud.base as task_crud
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

    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions)

    return task.get_validation_schema(
        is_correct=is_correct, user_attempts=user_attempts
    )


from features.tasks.schemas import BaseTaskRead
from features.solutions.models import BaseSolution


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
        session=session, account_id=account.id, task_ids=[task.id for task in tasks]
    )
    if not solutions:
        return [task.get_validation_schema() for task in tasks]

    solutions_by_task_id: dict[int, BaseSolution] = {
        sol.task_id: sol for sol in solutions
    }

    return [
        (
            task.get_validation_schema(
                is_correct=sol.is_correct,
                user_attempts=sol.user_attempts,
            )
            if (sol := solutions_by_task_id.get(task.id))
            else task.get_validation_schema()
        )
        for task in tasks
    ]


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
