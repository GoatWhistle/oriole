from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as base_solution_crud
from features.groups.validators import check_user_is_admin_or_owner, get_account_or_404
from features.modules.validators import get_module_or_404
from features.solutions.mappers import build_base_solution_read_list
from features.solutions.schemas import BaseSolutionRead
from features.solutions.validators import get_solution_or_404
from features.solutions.validators.membership import check_user_is_creator_of_solution
from features.spaces.validators import get_space_or_404
from features.tasks.models import BaseTask
from features.tasks.validators import get_task_or_404


async def get_solution(
    session: AsyncSession,
    user_id: int,
    solution_id: int,
) -> BaseSolutionRead:
    solution = await get_solution_or_404(session, solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_creator_of_solution(account, solution)
    return solution.get_validation_schema()


async def get_solutions_in_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> list[BaseSolutionRead]:
    task: BaseTask = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    solutions = await base_solution_crud.get_solutions_by_account_id_and_task_id(
        session, account.id, task_id
    )
    solutions = solutions or []
    return build_base_solution_read_list(solutions)


async def delete_solution(
    session: AsyncSession,
    user_id: int,
    solution_id: int,
) -> None:
    solution = await get_solution_or_404(session, solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    await base_solution_crud.delete_solution(session, solution)
