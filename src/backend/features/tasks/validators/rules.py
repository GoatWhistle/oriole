from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as crud
from features.tasks.exceptions import (
    TaskCounterLimitExceededException,
    TaskAlreadySolved,
    InvalidStringMatchTaskWithNumberConfiguration,
    InvalidStringMatchTaskWithStringConfiguration,
)
from features.tasks.models import BaseTask
from features.tasks.schemas import StringMatchTaskBase


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


def validate_string_match_task_configuration(task: StringMatchTaskBase) -> None:
    if task.compare_as_number:
        if task.is_case_sensitive is not None or task.normalize_whitespace is not None:
            raise InvalidStringMatchTaskWithNumberConfiguration()
    else:
        if task.is_case_sensitive is None or task.normalize_whitespace is None:
            raise InvalidStringMatchTaskWithStringConfiguration()
