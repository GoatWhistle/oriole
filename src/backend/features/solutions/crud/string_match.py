from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import StringMatchSolution
from features.solutions.schemas import StringMatchSolutionCreate
from utils import get_current_utc


async def create_string_match_solution(
    session: AsyncSession,
    solution_in: StringMatchSolutionCreate,
    is_correct: bool,
    account_id: int,
) -> StringMatchSolution:
    solution = StringMatchSolution(
        **solution_in.model_dump(),
        creator_id=account_id,
        is_correct=is_correct,
        submitted_at=get_current_utc(),
    )
    session.add(solution)
    await session.commit()
    await session.refresh(solution)
    return solution
