from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import MultipleChoiceSolution, BaseSolution
from features.solutions.schemas import MultipleChoiceFeedback
import features.solutions.crud.base as solutions_crud_base


async def create_feedback_to_multiple_choice_solution(
    session: AsyncSession,
    feedback: MultipleChoiceFeedback,
) -> MultipleChoiceSolution:
    current_solution = await solutions_crud_base.get_solution_by_id(
        session=session,
        solution_id=feedback.solution_id,
        solution_model=BaseSolution
    )
    current_solution.feedback = feedback.feedback
    await session.commit()
    return current_solution

