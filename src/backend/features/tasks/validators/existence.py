from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.string_match as task_crud
from features.tasks.exceptions import TaskNotFoundException
from features.tasks.models import StringMatchTask


async def get_task_or_404(
    session: AsyncSession,
    task_id: int,
) -> StringMatchTask:
    task = await task_crud.get_task_by_id(session, task_id)
    if not task:
        raise TaskNotFoundException()
    return task
