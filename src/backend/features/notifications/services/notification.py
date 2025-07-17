from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

import features.notifications.crud.notification as notification_crud
from features.notifications.mappers import build_notification_read_list
from features.notifications.schemas import NotificationRead
from features.users.validators import get_user_profile_if_exists


async def get_notification_by_id(
    session: AsyncSession,
    user_id: int,
    notification_id: int,
) -> NotificationRead:
    notification = await notification_crud.get_notification_by_id(session, notification_id)
    user = await get_user_profile_if_exists(session, user_id)
    if notification.user_id != user.user_id:
        raise PermissionError("User can only access their own notifications")
    return notification


async def get_user_notifications(
    session: AsyncSession,
    user_id: int,
    unread_only: bool = False,
) -> Sequence[NotificationRead]:
    user = await get_user_profile_if_exists(session, user_id)
    notifications = await notification_crud.get_user_notifications(
        session,
        user.user_id,
        unread_only=unread_only
    )
    return build_notification_read_list(notifications)


async def mark_notification_as_read(
    session: AsyncSession,
    user_id: int,
    notification_id: int,
) -> None:
    notification = await notification_crud.get_notification_by_id(session, notification_id)
    user = await get_user_profile_if_exists(session, user_id)
    if notification.user_id != user.user_id:
        raise PermissionError("User can only mark their own notifications as read")
    await notification_crud.mark_notification_as_read(session, notification_id)


async def mark_all_as_read(
    session: AsyncSession,
    user_id: int,
) -> None:
    user = await get_user_profile_if_exists(session, user_id)
    await notification_crud.mark_all_as_read(session, user.user_id)


async def get_unread_notifications_count(
    session: AsyncSession,
    user_id: int,
) -> int:
    user = await get_user_profile_if_exists(session, user_id)
    return await notification_crud.get_unread_notifications_count(session, user.user_id)


async def delete_notification(
    session: AsyncSession,
    user_id: int,
    notification_id: int,
) -> None:
    notification = await notification_crud.get_notification_by_id(session, notification_id)
    user = await get_user_profile_if_exists(session, user_id)
    if notification.user_id != user.user_id:
        raise PermissionError("User can only delete their own notifications")
    await notification_crud.delete_notification(session, notification)