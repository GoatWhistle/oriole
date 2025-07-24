from typing import Type

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import BaseSolution


async def get_solution_by_id(
    session: AsyncSession,
    solution_id: int,
    solution_model: Type[BaseSolution] = BaseSolution,
) -> BaseSolution | None:
    return await session.get(solution_model, solution_id)


async def get_solutions(
    session: AsyncSession,
    account_ids: list[int] | None = None,
    task_ids: list[int] | None = None,
) -> list[BaseSolution]:
    statement = select(BaseSolution)
    conditions = []

    if account_ids is not None:
        conditions.append(BaseSolution.creator_id.in_(account_ids))
    if task_ids is not None:
        conditions.append(BaseSolution.task_id.in_(task_ids))

    if conditions:
        statement = statement.where(*conditions)

    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_solutions_by_account_id_and_task_id(
    session: AsyncSession,
    account_id: int,
    task_id: int,
) -> list[BaseSolution]:
    solutions = await get_solutions(session, [account_id], [task_id])
    return list(solutions)


async def get_solutions_by_account_ids_and_task_ids(
    session: AsyncSession,
    account_ids: list[int],
    task_ids: list[int],
) -> list[BaseSolution]:
    return await get_solutions(session, account_ids, task_ids)


async def get_solutions_by_account_id_and_task_ids(
    session: AsyncSession,
    account_id: int,
    task_ids: list[int],
) -> list[BaseSolution]:
    return await get_solutions(session, [account_id], task_ids)


async def delete_solutions_by_task_id(session: AsyncSession, task_id: int) -> None:
    await session.execute(delete(BaseSolution).where(BaseSolution.task_id == task_id))
    await session.commit()


async def delete_solution(
    session: AsyncSession,
    solution: BaseSolution,
) -> None:
    await session.delete(solution)
    await session.commit()
