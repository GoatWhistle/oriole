from typing import Type

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_user_or_404(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user
