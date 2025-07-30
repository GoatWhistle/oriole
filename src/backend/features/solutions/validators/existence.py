from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as solution_crud
import features.solutions.crud.solution_feedback as solution_feedback_crud
from features.solutions.exceptions import (
    SolutionNotFoundException,
    SolutionFeedbackNotFoundException,
)
from features.solutions.models import BaseSolution, SolutionFeedback


async def get_solution_or_404(
    session: AsyncSession,
    solution_id: int,
    solution_model: Type[BaseSolution] = BaseSolution,
) -> BaseSolution:
    solution = await solution_crud.get_solution(session, solution_id, solution_model)
    if not solution:
        raise SolutionNotFoundException()
    return solution


async def get_solution_feedback_or_404(
    session: AsyncSession,
    solution_feedback_id: int,
) -> SolutionFeedback:
    solution_feedback = await solution_feedback_crud.get_solution_feedback(
        session, solution_feedback_id
    )
    if not solution_feedback:
        raise SolutionFeedbackNotFoundException()
    return solution_feedback
