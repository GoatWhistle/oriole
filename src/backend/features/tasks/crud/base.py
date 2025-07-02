from typing import Type, TypeVar, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from database import DbHelper
from features.tasks.models import BaseTask
from utils import get_current_utc


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
    task_model: Type[BaseTask] = BaseTask,
) -> BaseTask | None:
    return await session.get(task_model, task_id)


async def get_tasks(
    session: AsyncSession,
    task_model: Type[BaseTask] = BaseTask,
    is_active: bool | None = None,
) -> list[BaseTask]:
    statement = select(task_model)
    if is_active is not None:
        statement = statement.where(task_model.is_active == is_active)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_tasks_by_module_id(
    session: AsyncSession,
    module_id: int,
    is_active: bool | None = None,
    task_model: Type[BaseTask] = BaseTask,
) -> list[BaseTask]:
    return await get_tasks_by_module_ids(session, [module_id], is_active, task_model)


async def get_tasks_by_module_ids(
    session: AsyncSession,
    module_ids: list[int],
    is_active: bool | None = None,
    task_model: Type[BaseTask] = BaseTask,
) -> list[BaseTask]:
    statement = select(task_model).where(task_model.module_id.in_(module_ids))
    if is_active is not None:
        statement = statement.where(task_model.is_active == is_active)
    result = await session.execute(statement)
    return list(result.scalars().all())


TaskType = TypeVar("TaskType", bound=BaseTask)


async def update_task(
    session: AsyncSession,
    task: TaskType,
    task_update: dict[str, Any],
) -> TaskType:
    for key, value in task_update.items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task


async def update_tasks_activity():
    local_db_helper = DbHelper(url=str(settings.db.url))

    async with local_db_helper.session_factory() as session:
        tasks = await get_tasks(session)

        updated = False
        for task in tasks:
            new_status = task.start_datetime <= get_current_utc() <= task.end_datetime
            if task.is_active != new_status:
                task.is_active = new_status
                updated = True

        if updated:
            await session.commit()

        await local_db_helper.dispose()


async def delete_task(
    session: AsyncSession,
    task: BaseTask,
) -> None:
    await session.delete(task)
    await session.commit()
