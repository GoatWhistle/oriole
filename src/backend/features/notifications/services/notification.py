from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

import features.notifications.crud.notification as notification_crud
from features.notifications.crud.notification_settings import get_settings
from features.notifications.mappers import build_notification_read_list
from features.notifications.schemas import NotificationRead, NotificationCreate
from features.notifications.services.notification_settings import gen_blacklist
from features.notifications.services.telegram_notifier import send_personal_notification
from features.users.validators import get_user_profile_if_exists
from shared.enums import NotificationTypeEnum

from sqlalchemy import select
from features.notifications.models import Notification


async def get_notification_by_id(
        session: AsyncSession,
        user_id: int,
        notification_id: int,
) -> NotificationRead | None:
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


async def send_notification(
        session: AsyncSession,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationTypeEnum,
        entity_id: int | None = None,
) -> bool:
    settings = await get_settings(session, user_id)
    if notification_type in gen_blacklist(settings):
        return False
    notification = NotificationCreate(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        related_entity_id=entity_id
    )
    await notification_crud.create_notification(session=session, notification_in=notification)

    if settings.telegram_enabled:
        await send_personal_notification(
            session=session,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            entity_id=entity_id
        )

    return True


async def was_notification_sent(
        session: AsyncSession,
        task_id: int,
        notification_type: NotificationTypeEnum,
        within_hours: float | None = None
) -> bool:
    stmt = select(Notification).where(
        Notification.related_entity_id == task_id,
        Notification.notification_type == notification_type.value
    )

    if within_hours is not None:
        from sqlalchemy import func
        time_threshold = func.now() - func.make_interval(hours=within_hours)
        stmt = stmt.where(Notification.created_at >= time_threshold)

    result = await session.execute(stmt.limit(1))
    return result.scalar() is not None
