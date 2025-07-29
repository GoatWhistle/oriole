from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.feedback_multiple as multiple_choice_solution_feedback_crud
from features.groups.validators import get_account_or_404
from features.modules.validators import get_module_or_404
from features.solutions.schemas import MultipleChoiceFeedback
from features.spaces.validators import get_space_or_404
from features.tasks.models import MultipleChoice
from features.tasks.validators import (
    check_counter_limit,
    get_task_or_404,
    validate_solution_creation,
)
from shared.validators import check_is_active


async def create_feedback_multiple_choice_solution(
    session: AsyncSession,
    user_id: int,
    feedback_in: MultipleChoiceFeedback,
):
    task = await get_task_or_404(session, feedback_in.task_id, MultipleChoice)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_is_active(task.is_active)
    total_attempts = await validate_solution_creation(session, account.id, task)
    check_counter_limit(task.max_attempts, total_attempts)

    feedback = (
        await multiple_choice_solution_feedback_crud.create_string_match_solution(
            session, feedback_in, account.id
        )
    )

    return feedback.get_validation_schema()
