from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.assignment import Assignment
from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentUpdate,
    AssignmentUpdatePartial,
)


async def create_assignment(
    session: AsyncSession,
    assignment_in: AssignmentCreate,
) -> AssignmentRead:
    assignment = AssignmentRead(**assignment_in.model_dump())
    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)
    return assignment


async def get_assignments(
    session: AsyncSession,
) -> Sequence[Assignment]:
    statement = select(Assignment).order_by(Assignment.id)
    result: Result = await session.execute(statement)
    return list(result.scalars().all())


async def get_assignment(
    session: AsyncSession,
    assignment_id: int,
) -> Assignment | None:
    return await session.get(Assignment, assignment_id)


async def update_assignment(
    session: AsyncSession,
    assignment: Assignment,
    assignment_update: AssignmentUpdate | AssignmentUpdatePartial,
    partial: bool = False,
) -> Assignment:
    for name, value in assignment_update.model_dump(exclude_unset=partial).items():
        setattr(assignment, name, value)
    await session.commit()
    return assignment


async def delete_assignment(
    session: AsyncSession,
    assignment: Assignment,
) -> None:
    await session.delete(assignment)
    await session.commit()
