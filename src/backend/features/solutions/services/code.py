from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as base_solution_crud
import features.solutions.crud.code as code_solution_crud
from core.celery.code_check_task import check_code
from features import CodeTask
from features.groups.validators import get_group_or_404, get_account_or_404
from features.modules.validators import get_module_or_404
from features.solutions.schemas import CodeSolutionCreate, CodeSolutionRead
from features.solutions.validators.existence import get_solution_or_404
from features.solutions.validators.membership import check_user_is_creator_of_solution
from features.tasks.validators import get_task_or_404
from features.tasks.validators.existence import get_tests_or_404
from shared.validators import check_is_active
from utils.code_check import get_runtime_or_404


async def create_code_solution(
    session: AsyncSession,
    user_id: int,
    solution_in: CodeSolutionCreate,
    language: str,
) -> CodeSolutionRead:
    task = cast(
        CodeTask,
        await get_task_or_404(session, solution_in.task_id, CodeTask),
    )
    runtime = get_runtime_or_404(language)
    module = await get_module_or_404(session, task.module_id)
    group = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)
    tests = await get_tests_or_404(session, task.id)

    check_is_active(task.is_active)

    solution = await code_solution_crud.create_solution(
        session, solution_in, account.id
    )
    check_code.delay(solution.id, runtime)
    return CodeSolutionRead.model_validate(solution)


async def get_code_solution_by_id(
    session: AsyncSession,
    user_id: int,
    solution_id: int,
):
    solution = await get_solution_or_404(session, solution_id)
    task = await get_task_or_404(session, solution.task_id, task_model=CodeTask)
    module = await get_module_or_404(session, task.module_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_creator_of_solution(account, solution)
    return CodeSolutionRead.model_validate(solution)


async def get_user_solutions_by_task_id(
    session: AsyncSession,
    user_id: int,
    task_id: int,
):
    task = await get_task_or_404(session, task_id, task_model=CodeTask)
    module = await get_module_or_404(session, task.module_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    solutions = await base_solution_crud.get_solutions_by_account_id_and_task_id(
        session,
        account.id,
        task_id,
    )
    solutions = solutions or []
    return [CodeSolutionRead.model_validate(solution) for solution in solutions]
