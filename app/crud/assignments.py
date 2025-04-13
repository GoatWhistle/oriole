from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.assignment import get_assignment_or_404

from core.models import Task, Assignment

from core.schemas.task import TaskRead

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
    assignment = Assignment(**assignment_in.model_dump())
    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)

    return AssignmentRead.model_validate(assignment)


async def get_assignment(
    session: AsyncSession,
    assignment_id: int,
) -> AssignmentRead:
    assignment = await get_assignment_or_404(
        session=session, assignment_id=assignment_id
    )
    return AssignmentRead.model_validate(assignment)


async def get_assignments(
    session: AsyncSession,
    group_id: int,
) -> Sequence[AssignmentRead]:
    statement = (
        select(Assignment)
        .where(Assignment.group_id == group_id)
        .order_by(Assignment.id)
    )

    result: Result = await session.execute(statement)
    assignments = list(result.scalars().all())

    return [AssignmentRead.model_validate(assignment) for assignment in assignments]


async def update_assignment(
    session: AsyncSession,
    assignment_id: int,
    assignment_update: AssignmentUpdate | AssignmentUpdatePartial,
    partial: bool = False,
) -> AssignmentRead:
    assignment = await get_assignment_or_404(
        session=session, assignment_id=assignment_id
    )
    for name, value in assignment_update.model_dump(exclude_unset=partial).items():
        setattr(assignment, name, value)

    await session.commit()
    await session.refresh(assignment)

    return AssignmentRead.model_validate(assignment)


async def delete_assignment(
    session: AsyncSession,
    assignment_id: int,
) -> None:
    assignment = await get_assignment_or_404(
        session=session, assignment_id=assignment_id
    )
    await session.delete(assignment)
    await session.commit()


async def get_tasks_in_assignment(
    session: AsyncSession,
    assignment_id: int,
) -> Sequence[TaskRead]:
    statement = (
        select(Task).where(Task.assignment_id == assignment_id).order_by(Task.id)
    )

    result: Result = await session.execute(statement)
    tasks = list(result.scalars().all())

    return [TaskRead.model_validate(task) for task in tasks]
