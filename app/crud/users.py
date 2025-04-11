from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Group
from core.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> UserRead:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.from_orm(user)


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
