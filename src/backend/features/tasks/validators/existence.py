from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.task as task_crud
from features.tasks.exceptions import TaskNotFoundException
from features.tasks.models import Task


async def get_task_or_404(
    session: AsyncSession,
    task_id: int,
) -> Task:
    task = await task_crud.get_task_by_id(session, task_id)
    if not task:
        raise TaskNotFoundException()
    return task
