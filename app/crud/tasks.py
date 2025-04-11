from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task

from core.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
)


async def create_task(
    session: AsyncSession,
    task_in: TaskCreate,
) -> TaskRead:
    task = TaskRead(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskRead.model_validate(task)


async def get_task(
    session: AsyncSession,
    task_id: int,
) -> TaskRead | None:
    task = await session.get(Task, task_id)

    return None if task is None else TaskRead.model_validate(task)


async def get_tasks(
    session: AsyncSession,
    assignment_id: int,
) -> Sequence[TaskRead]:
    statement = (
        select(Task).where(Task.assignment_id == assignment_id).order_by(Task.id)
    )

    result: Result = await session.execute(statement)
    tasks = list(result.scalars().all())

    return [TaskRead.model_validate(task) for task in tasks]


async def update_task(
    session: AsyncSession,
    task: TaskRead,
    task_update: TaskUpdate | TaskUpdatePartial,
    partial: bool = False,
) -> TaskRead:
    for name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, name, value)
    await session.commit()
    await session.refresh(task)

    return TaskRead.model_validate(task)


async def delete_task(
    session: AsyncSession,
    task: TaskRead,
) -> None:
    await session.delete(task)
    await session.commit()
