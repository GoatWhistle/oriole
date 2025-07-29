from sqlalchemy.ext.asyncio import AsyncSession

from features.notifications.models.notification_settings import UserNotificationSettings
from features.notifications.schemas.notification_settings import (
    UserNotificationSettingsUpdate,
)
from features.notifications.crud import (
    notification_settings as notification_settings_crud,
)
from shared.enums import NotificationTypeEnum


async def update_notification_settings(
    session: AsyncSession, user_id: int, settings_update: UserNotificationSettingsUpdate
) -> UserNotificationSettings:
    return await notification_settings_crud.update_settings(
        session, user_id, settings_update
    )


def gen_blacklist(settings: UserNotificationSettings):
    blacklist = list()
    if not settings.chat_notifications_enabled:
        blacklist.append(NotificationTypeEnum.CHAT_MESSAGE)
    if not settings.deadline_notifications_enabled:
        blacklist.append(
            [
                NotificationTypeEnum.DEADLINE_OVERDUE,
                NotificationTypeEnum.DEADLINE_1H,
                NotificationTypeEnum.DEADLINE_24H,
            ]
        )
    if not settings.system_notifications_enabled:
        blacklist.append(NotificationTypeEnum.BASE)
    return blacklist
