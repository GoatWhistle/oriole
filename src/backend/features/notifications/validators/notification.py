from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from features.notifications.models import Notification
from features.users.validators import get_user_profile_if_exists


async def get_notification_or_404(
    session: AsyncSession,
    notification_id: int,
) -> Notification or None:
    notification = await session.get(Notification, notification_id)
    if not notification:
        raise ValueError(f"Notification with id {notification_id} not found")
    return notification


async def check_user_owns_notification(
    session: AsyncSession,
    user_id: int,
    notification_id: int,
) -> Notification or None:
    user = await get_user_profile_if_exists(session, user_id)
    notification = await get_notification_or_404(session, notification_id)

    if notification.user_id != user.user_id:
        raise PermissionError(
            "User does not have permission to access this notification"
        )

    return notification


async def validate_notification_creation(
    session: AsyncSession,
    user_id: int,
    notification_data: dict,
) -> None:
    user = await get_user_profile_if_exists(session, user_id)

    if not notification_data.get("title"):
        raise ValueError("Notification title cannot be empty")

    if not notification_data.get("message"):
        raise ValueError("Notification message cannot be empty")

    if len(notification_data["title"]) > 100:
        raise ValueError("Notification title is too long (max 100 characters)")

    if len(notification_data["message"]) > 500:
        raise ValueError("Notification message is too long (max 500 characters)")

    if not user:
        raise ValueError("User not found")
