from typing import Type

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task


async def get_group_or_404(session: AsyncSession, task_id: int) -> Type[Task]:
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task
