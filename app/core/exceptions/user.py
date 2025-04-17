from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import User

from core.schemas.user import (
    RegisterUser,
)


async def get_user_or_404_with_return(
    session: AsyncSession, user_id: int
) -> Type[User]:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user


async def get_user_or_404(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )


# TODO: добавить роль teacher
async def check_teacher_or_403(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if not (user.is_teacher or user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires teacher or admin privileges",
        )
    return user
