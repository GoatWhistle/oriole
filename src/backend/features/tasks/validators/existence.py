from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.task as task_crud
from features.tasks.models import Task


async def get_task_if_exists(
    session: AsyncSession,
    task_id: int,
) -> Task:
    task = await task_crud.get_task_by_id(session, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} does not exist",
        )
    return task
