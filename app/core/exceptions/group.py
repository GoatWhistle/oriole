from typing import Type

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Group


async def get_group_or_404(session: AsyncSession, group_id: int) -> Type[Group]:
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail=f"Group {group_id} not found")
    return group
