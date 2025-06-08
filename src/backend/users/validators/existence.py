from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User


async def check_user_exists(
    session: AsyncSession,
    user_id: int,
) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} does not exist",
        )
