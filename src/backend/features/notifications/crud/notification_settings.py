from sqlalchemy.ext.asyncio import AsyncSession

from features.notifications.models.notification_settings import UserNotificationSettings
from features.notifications.schemas.notification_settings import (
    UserNotificationSettingsUpdate,
)


async def get_settings(
    session: AsyncSession,
    user_id: int,
) -> UserNotificationSettings | None:
    return await session.get(UserNotificationSettings, user_id)


async def create_settings(
    session: AsyncSession,
    user_id: int,
) -> UserNotificationSettings:
    settings = UserNotificationSettings(user_id=user_id)
    session.add(settings)
    await session.commit()
    await session.refresh(settings)
    return settings


async def update_settings(
    session: AsyncSession, user_id: int, settings_update: UserNotificationSettingsUpdate
) -> UserNotificationSettings:
    settings = await get_settings(session=session, user_id=user_id)
    if not settings:
        settings = await create_settings(session, user_id)

    update_data = settings_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(settings, key, value)

    await session.commit()
    await session.refresh(settings)
    return settings
