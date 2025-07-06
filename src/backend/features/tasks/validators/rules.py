from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as crud
from features.tasks.exceptions import (
    TaskCounterLimitExceededException,
    TaskAlreadySolved,
)
from features.tasks.models import BaseTask


def check_counter_limit(
    task_max_attempts: int,
    user_reply_attempts: int,
) -> None:
    if user_reply_attempts >= task_max_attempts:
        raise TaskCounterLimitExceededException()


async def validate_solution_creation(
    session: AsyncSession,
    account_id: int,
    task: BaseTask,
) -> int:
    solutions = await crud.get_solutions_by_account_id_and_task_id(
        session, account_id, task.id
    )

    total_attempts = len(solutions)
    is_correct = any(sol.is_correct for sol in solutions)

    if is_correct and not task.can_attempt:
        raise TaskAlreadySolved()

    return total_attempts
