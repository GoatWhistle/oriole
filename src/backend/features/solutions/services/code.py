from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.code as code_solution_crud
from core.celery.code_check_task import check_code
from features.groups.validators import get_account_or_404, get_group_or_404
from features.modules.validators import get_module_or_404
from features.solutions.schemas import CodeSolutionCreate, CodeSolutionRead
from features.solutions.validators import (
    validate_solution_after_creation,
    validate_solution_before_creation,
)
from features.tasks.models import CodeTask
from features.tasks.validators import get_task_or_404
from features.tasks.validators.existence import get_tests_or_404


async def create_code_solution(
    session: AsyncSession,
    user_id: int,
    solution_in: CodeSolutionCreate,
) -> CodeSolutionRead:
    task = cast(CodeTask, await get_task_or_404(session, solution_in.task_id, CodeTask))
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)
    _ = await get_tests_or_404(session, task.id)

    await validate_solution_before_creation(session, account.id, task)

    solution = await code_solution_crud.create_solution(
        session, solution_in, account.id
    )

    await validate_solution_after_creation(session, account.id, task, solution)

    check_code.delay(solution.id)

    return solution.get_validation_schema()
