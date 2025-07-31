from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.account_task_progress as progress_crud
from features.solutions.models import BaseSolution
from features.tasks.exceptions import (
    TaskAlreadySolved,
    TaskCounterLimitExceededException,
    TaskInactiveException,
)
from features.tasks.models import BaseTask


async def validate_solution_before_creation(
    session: AsyncSession,
    account_id: int,
    task: BaseTask,
) -> None:
    account_task_progress = (
        await progress_crud.get_account_task_progress_by_account_and_task_id(
            session, account_id, task.id
        )
    )
    if account_task_progress is None:
        account_task_progress = progress_crud.create_account_task_progress(
            session, account_id, task.id, False, 0
        )

    if not task.is_active:
        raise TaskInactiveException()

    if account_task_progress.user_attempts >= task.max_attempts:
        raise TaskCounterLimitExceededException()

    if account_task_progress.is_correct and not task.can_attempt:
        raise TaskAlreadySolved()


async def validate_solution_after_creation(
    session: AsyncSession,
    account_id: int,
    task: BaseTask,
    solution: BaseSolution,
) -> None:
    account_task_progress = (
        await progress_crud.get_account_task_progress_by_account_and_task_id(
            session, account_id, task.id
        )
    )

    await progress_crud.increment_user_attempts_count(session, account_task_progress)

    if solution.is_correct and not account_task_progress.is_correct:
        await progress_crud.change_is_correct_status(
            session, account_task_progress, solution.is_correct
        )
