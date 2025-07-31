from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.multiple_choice as multiple_choice_solution_crud
from features.groups.validators import get_account_or_404
from features.modules.validators import get_module_or_404
from features.solutions.schemas import (
    MultipleChoiceSolutionCreate,
    MultipleChoiceSolutionRead,
)
from features.solutions.validators import (
    validate_solution_after_creation,
    validate_solution_before_creation,
)
from features.spaces.validators import get_space_or_404
from features.tasks.models import MultipleChoiceTask
from features.tasks.validators import get_task_or_404


async def create_multiple_choice_solution(
    session: AsyncSession,
    user_id: int,
    solution_in: MultipleChoiceSolutionCreate,
) -> MultipleChoiceSolutionRead:
    task = await get_task_or_404(session, solution_in.task_id, MultipleChoiceTask)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    await validate_solution_before_creation(session, account.id, task)

    solution = await multiple_choice_solution_crud.create_multiple_choice_solution(
        session, solution_in, account.id, cast(MultipleChoiceTask, task).correct_answer
    )

    await validate_solution_after_creation(session, account.id, task, solution)

    return solution.get_validation_schema()
