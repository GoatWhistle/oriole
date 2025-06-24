from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from features.users.models import User
from features.users.schemas import (
    RegisterUserInput,
    RegisterUserInternal,
)
from utils.JWT import (
    hash_password,
)


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(
    session: AsyncSession,
    email: EmailStr,
) -> User | None:
    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    return user_from_db


async def create_user(
    session: AsyncSession,
    user_data: RegisterUserInput,
) -> User:
    internal_data = RegisterUserInternal(**user_data.model_dump())
    internal_data.is_active = True
    internal_data.is_verified = False

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=internal_data.is_active,
        is_verified=internal_data.is_verified,
    )
    session.add(user)
    await session.flush()

    return user


async def update_user_verification_status(
    session: AsyncSession,
    user: User,
) -> User:
    user.is_verified = True
    await session.commit()
    await session.refresh(user)

    return user


async def update_user_password(
    session: AsyncSession,
    user: User,
    new_password: str,
) -> User:
    user.hashed_password = hash_password(new_password)
    await session.commit()
    await session.refresh(user)

    return user
