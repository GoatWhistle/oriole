from typing import Type

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Assignment


async def get_group_or_404(
    session: AsyncSession, assignment_id: int
) -> Type[Assignment]:
    assignment = await session.get(Assignment, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=404, detail=f"Assignment {assignment_id} not found"
        )
    return assignment
