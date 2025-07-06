from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models.code import CodeSolution
from features.solutions.schemas import CodeSolutionCreate


async def create_solution(
    session: AsyncSession,
    solution_in: CodeSolutionCreate,
    user_id: int,
) -> CodeSolution:
    solution = CodeSolution(**solution_in.model_dump())
    solution.account_id = user_id
    session.add(solution)
    await session.commit()
    await session.refresh(solution)
    return solution
