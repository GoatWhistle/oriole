from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import StringMatchSolution
from features.solutions.schemas import StringMatchSolutionCreate
from utils import get_current_utc


async def create_string_match_solution(
    session: AsyncSession,
    solution_in: StringMatchSolutionCreate,
    account_id: int,
    correct_answer: str,
) -> StringMatchSolution:
    solution = StringMatchSolution(
        **solution_in.model_dump(),
        account_id=account_id,
        is_correct=(solution_in.user_answer == correct_answer),
        submitted_at=get_current_utc(),
    )
    session.add(solution)
    await session.commit()
    await session.refresh(solution)
    return solution


async def delete_string_match_solution(
    session: AsyncSession,
    string_match_solution: StringMatchSolution,
) -> None:
    await session.delete(string_match_solution)
    await session.commit()
