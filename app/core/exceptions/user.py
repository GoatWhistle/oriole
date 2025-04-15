from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import User

from core.schemas.user import UserCreate, UserRead, UserUpdate, UserAuth, RegisterUser


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


# TODO: добавить роль teacher
async def check_teacher_or_403(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if not (user.is_teacher or user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires teacher or admin privileges",
        )
    return user


async def if_already_registered(
    session: AsyncSession,
    user_data: RegisterUser,
) -> None:
    user = await session.get(User, user_data)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with '{user_data.email}' email has already registered",
        )
