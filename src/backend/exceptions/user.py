from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from core.schemas.user import UserAuthRead


async def check_user_exists(
    session: AsyncSession,
    user_id: int,
) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )


async def validate_activity_and_verification(
    user_from_db: UserAuthRead,
):
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    if not user_from_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    if not user_from_db.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is unverified",
        )
