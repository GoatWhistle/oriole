from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.base as solution_crud
from features.solutions.exceptions import SolutionNotFoundException
from features.solutions.models import BaseSolution


async def get_solution_or_404(
    session: AsyncSession,
    solution_id: int,
    solution_model: Type[BaseSolution] = BaseSolution,
) -> BaseSolution:
    solution = await solution_crud.get_solution_by_id(
        session, solution_id, solution_model
    )
    if not solution:
        raise SolutionNotFoundException()
    return solution
