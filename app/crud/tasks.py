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
    return task


async def get_tasks(
    session: AsyncSession,
) -> Sequence[Task]:
    statement = select(Task).order_by(Task.id)
    result: Result = await session.execute(statement)
    return list(result.scalars().all())


async def get_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    return await session.get(Task, task_id)


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: TaskUpdate | TaskUpdatePartial,
    partial: bool = False,
) -> Task:
    for name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, name, value)
    await session.commit()
    return task


async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    await session.delete(task)
    await session.commit()
