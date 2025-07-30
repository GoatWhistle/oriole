from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import MultipleChoiceSolution
from features.solutions.schemas import MultipleChoiceSolutionCreate
from utils import get_current_utc


async def create_multiple_choice_solution(
    session: AsyncSession,
    solution_in: MultipleChoiceSolutionCreate,
    account_id: int,
    correct_answer: list,
) -> MultipleChoiceSolution:
    solution = MultipleChoiceSolution(
        **solution_in.model_dump(),
        creator_id=account_id,
        is_correct=(set(solution_in.user_answer) == set(correct_answer)),
        submitted_at=get_current_utc(),
    )
    session.add(solution)
    await session.commit()
    await session.refresh(solution)
    return solution
