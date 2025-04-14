from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Group


async def check_group_exists(session: AsyncSession, group_id: int) -> None:
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} not found",
        )
