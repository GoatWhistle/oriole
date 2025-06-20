from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import Task
from features.tasks.schemas import TaskCreate, TaskUpdate, TaskUpdatePartial
from utils import get_current_utc


async def create_task(
    session: AsyncSession,
    task_data: TaskCreate,
) -> Task:
    is_active = task_data.start_datetime <= get_current_utc() <= task_data.end_datetime
    task = Task(
        **task_data.model_dump(exclude={"is_active"}),
        is_active=is_active,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


def clone_task_to_module(
    source: Task,
    module_id: int,
) -> Task:
    return Task(
        title=source.title,
        description=source.description,
        correct_answer=source.correct_answer,
        is_active=source.is_active,
        module_id=module_id,
        max_attempts=source.max_attempts,
        start_datetime=source.start_datetime,
        end_datetime=source.end_datetime,
    )


async def clone_tasks_to_module(
    session: AsyncSession,
    source_tasks: Sequence[Task],
    module_id: int,
) -> Sequence[Task]:
    new_tasks = [clone_task_to_module(task, module_id) for task in source_tasks]
    session.add_all(new_tasks)
    for task in new_tasks:
        await session.refresh(task)
    await session.commit()
    return new_tasks


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    return await session.get(Task, task_id)


async def get_tasks(
    session: AsyncSession,
    is_active: bool | None = None,
) -> Sequence[Task]:
    statement = select(Task)
    if is_active is not None:
        statement = statement.where(Task.is_active == is_active)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_tasks_by_module_id(
    session: AsyncSession,
    module_id: int,
    is_active: bool | None = None,
) -> Sequence[Task]:
    return await get_tasks_by_module_ids(session, [module_id], is_active)


async def get_tasks_by_module_ids(
    session: AsyncSession,
    module_ids: Sequence[int],
    is_active: bool | None = None,
) -> Sequence[Task]:
    statement = select(Task).where(Task.module_id.in_(module_ids))
    if is_active is not None:
        statement = statement.where(Task.is_active == is_active)
    result = await session.execute(statement)
    return result.scalars().all()


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: TaskUpdate | TaskUpdatePartial,
) -> Task:
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    await session.delete(task)
    await session.commit()
