from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.users.models import User, UserProfile
from features.users.schemas.telegram_user import TelegramUserData


async def get_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_user_via_telegram(
    session: AsyncSession,
    user_data: TelegramUserData,
) -> User:
    user = User(
        telegram_id=user_data.id,
        email=None,
        hashed_password=None,
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )
    session.add(user)
    await session.flush()

    profile = UserProfile(
        user_id=user.id,
        name=user_data.first_name or "TelegramUser",
        surname=user_data.last_name or "",
        patronymic="",
    )
    session.add(profile)
    await session.flush()

    await session.commit()

    return user
