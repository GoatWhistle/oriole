from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.models import Task


async def check_task_exists(
    session: AsyncSession,
    task_id: Mapped[int] | int,
) -> None:
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
