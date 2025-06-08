from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from features.tasks.models import Task


async def get_task_if_exists(
    session: AsyncSession,
    task_id: int | Mapped[int],
) -> Task | Type[Task]:
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} does not exist",
        )
    return task
