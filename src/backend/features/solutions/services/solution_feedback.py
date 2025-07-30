from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.solution_feedback as solution_feedback_crud
from features.groups.validators import get_account_or_404, check_user_is_admin_or_owner
from features.modules.validators import get_module_or_404
from features.solutions.mappers import build_base_solution_feedback_read_list
from features.solutions.schemas import (
    SolutionFeedbackRead,
    SolutionFeedbackCreate,
    SolutionFeedbackUpdate,
)
from features.solutions.validators import (
    get_solution_or_404,
    get_solution_feedback_or_404,
)
from features.spaces.validators import get_space_or_404
from features.tasks.validators import get_task_or_404


async def create_solution_feedback(
    session: AsyncSession,
    user_id: int,
    solution_id: int,
    solution_feedback_create: SolutionFeedbackCreate,
) -> SolutionFeedbackRead:
    solution = await get_solution_or_404(session, solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    solution_feedback = await solution_feedback_crud.create_solution_feedback(
        session, solution_feedback_create, solution_id, account.id
    )

    return solution_feedback.get_validation_schema()


async def get_solution_feedback(
    session: AsyncSession,
    user_id: int,
    solution_feedback_id: int,
) -> SolutionFeedbackRead:
    solution_feedback = await get_solution_feedback_or_404(
        session, solution_feedback_id
    )
    solution = await get_solution_or_404(session, solution_feedback.solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    _ = await get_account_or_404(session, user_id, module.space_id)

    return solution_feedback.get_validation_schema()


async def get_feedbacks_by_solution_id(
    session: AsyncSession,
    user_id: int,
    solution_id: int,
) -> list[SolutionFeedbackRead]:
    solution = await get_solution_or_404(session, solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    _ = await get_account_or_404(session, user_id, module.space_id)

    solution_feedbacks = await solution_feedback_crud.get_feedbacks_by_solution_id(
        session, solution_id
    )
    return build_base_solution_feedback_read_list(solution_feedbacks)


async def update_multiple_choice_task(
    session: AsyncSession,
    user_id: int,
    solution_feedback_id: int,
    solution_feedback_update: SolutionFeedbackUpdate,
) -> SolutionFeedbackRead:
    solution_feedback = await get_solution_feedback_or_404(
        session, solution_feedback_id
    )
    solution = await get_solution_or_404(session, solution_feedback.solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = solution_feedback_update.model_dump(exclude_unset=True)

    solution_feedback = await solution_feedback_crud.update_solution_feedback(
        session, solution_feedback, update_data
    )

    return solution_feedback.get_validation_schema()


async def delete_solution_feedback(
    session: AsyncSession,
    user_id: int,
    solution_feedback_id: int,
) -> None:
    solution_feedback = await get_solution_feedback_or_404(
        session, solution_feedback_id
    )
    solution = await get_solution_or_404(session, solution_feedback.solution_id)
    task = await get_task_or_404(session, solution.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    await solution_feedback_crud.delete_solution_feedback(session, solution_feedback)
