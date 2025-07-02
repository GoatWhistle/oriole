from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.base as task_crud
from features import BaseTask
from features.tasks.exceptions import TaskNotFoundException


async def get_task_or_404(
    session: AsyncSession,
    task_id: int,
) -> BaseTask:
    task = await task_crud.get_task_by_id(session, task_id)
    if not task:
        raise TaskNotFoundException()
    return task
