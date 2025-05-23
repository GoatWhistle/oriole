from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.models import Assignment


async def get_assignment_if_exists(
    session: AsyncSession,
    assignment_id: Mapped[int] | int,
) -> Assignment:
    assignment = await session.get(Assignment, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment {assignment_id} not found",
        )
    return assignment
