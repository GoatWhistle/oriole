from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.account_module_progress as module_progress_crud
import features.tasks.crud.account_task_progress as task_progress_crud
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
        await task_progress_crud.get_account_task_progress_by_account_id_and_task_id(
            session, account_id, task.id
        )
    )
    account_module_progress = await module_progress_crud.get_account_module_progress_by_account_id_and_module_id(
        session, account_id, task.module_id
    )

    if account_task_progress is None:
        account_task_progress = await task_progress_crud.create_account_task_progress(
            session, account_id, task.id, False, 0
        )

    if account_module_progress is None:
        await module_progress_crud.create_account_module_progress(
            session, account_id, task.module_id, 0
        )

    if not task.is_active:
        raise TaskInactiveException()

    if account_task_progress.user_attempts_count >= task.max_attempts:
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
        await task_progress_crud.get_account_task_progress_by_account_id_and_task_id(
            session, account_id, task.id
        )
    )
    account_module_progress = await module_progress_crud.get_account_module_progress_by_account_id_and_module_id(
        session, account_id, task.module_id
    )

    await task_progress_crud.increment_user_attempts_count(
        session, account_task_progress
    )

    if solution.is_correct and not account_task_progress.is_correct:
        await task_progress_crud.change_is_correct_status(
            session, account_task_progress, solution.is_correct
        )
        await module_progress_crud.increment_user_completed_tasks_count(
            session, account_module_progress
        )
