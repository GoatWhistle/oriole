import re
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.string_match as string_match_solution_crud
from features import StringMatchTask
from features.groups.validators import get_account_or_404
from features.modules.validators import get_module_or_404
from features.solutions.schemas import (
    StringMatchSolutionRead,
    StringMatchSolutionCreate,
)
from features.spaces.validators import get_space_or_404
from features.tasks.validators import (
    check_counter_limit,
    get_task_or_404,
    validate_solution_creation,
)
from shared.validators import check_is_active


def compare_as_numbers(correct: str, user: str) -> bool:
    correct = float(correct.replace(",", "."))
    user = float(user.replace(",", "."))
    return correct == user


def compare_as_strings(correct: str, user: str, task: StringMatchTask) -> bool:
    if task.normalize_whitespace:
        correct = re.sub(r"\s+", " ", correct.strip())
        user = re.sub(r"\s+", " ", user.strip())
    if not task.is_case_sensitive:
        correct = correct.lower()
        user = user.lower()
    return correct == user


async def create_string_match_solution(
    session: AsyncSession,
    user_id: int,
    solution_in: StringMatchSolutionCreate,
) -> StringMatchSolutionRead:
    task = cast(
        StringMatchTask,
        await get_task_or_404(session, solution_in.task_id, StringMatchTask),
    )
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_is_active(task.is_active)
    total_attempts = await validate_solution_creation(session, account.id, task)
    check_counter_limit(task.max_attempts, total_attempts)

    if task.compare_as_number:
        is_correct = compare_as_numbers(task.correct_answer, solution_in.user_answer)
    else:
        is_correct = compare_as_strings(
            task.correct_answer, solution_in.user_answer, task
        )

    solution = await string_match_solution_crud.create_string_match_solution(
        session, solution_in, is_correct, account.id
    )

    return solution.get_validation_schema()
