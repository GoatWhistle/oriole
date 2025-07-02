from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.base as task_crud
from features.tasks.exceptions import TaskNotFoundException
from features.tasks.models import BaseTask


async def get_task_or_404(
    session: AsyncSession,
    task_id: int,
    task_model: Type[BaseTask] = BaseTask,
) -> BaseTask:
    task = await task_crud.get_task_by_id(session, task_id, task_model)
    if not task:
        raise TaskNotFoundException()
    return task
