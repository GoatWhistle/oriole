from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as base_solution_crud
import features.solutions.crud.string_match as string_match_solution_crud
from features import StringMatchTask
from features.groups.validators import get_group_or_404, get_account_or_404
from features.modules.validators import get_module_or_404
from features.tasks.schemas.string_match import StringMatchTaskRead
from features.tasks.validators import check_counter_limit
from features.tasks.validators import get_task_or_404
from shared.validators import check_is_active


async def create_string_match_solution(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    user_answer: str,
) -> StringMatchTaskRead:
    task = cast(
        StringMatchTask, await get_task_or_404(session, task_id, StringMatchTask)
    )
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_is_active(task.is_active)

    solutions = await base_solution_crud.get_solutions_by_account_id_and_task_id(
        session, account.id, task.id
    )

    total_attempts = len(solutions)
    is_already_correct = any(sol.is_correct for sol in solutions)

    if not task.can_attempt and is_already_correct:
        return task.get_validation_schema(
            is_correct=True,
            user_attempts=total_attempts,
        )

    check_counter_limit(task.max_attempts, total_attempts)

    new_solution = await string_match_solution_crud.create_string_match_solution(
        session, account.id, task, user_answer
    )

    return task.get_validation_schema(
        is_correct=new_solution.is_correct or is_already_correct,
        user_attempts=total_attempts + 1,
    )
