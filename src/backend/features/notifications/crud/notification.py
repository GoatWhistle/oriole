from typing import Sequence, Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from features.notifications.models import Notification
from features.notifications.schemas import NotificationCreate


async def create_notification(
    session: AsyncSession,
    notification_in: NotificationCreate,
) -> Notification:
    notification = Notification(**notification_in.model_dump())
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    return notification


async def get_notification_by_id(
    session: AsyncSession,
    notification_id: int,
) -> Notification | None:
    return await session.get(Notification, notification_id)


async def get_user_notifications(
    session: AsyncSession,
    user_id: int,
    limit: int = 100,
    unread_only: bool = False,
) -> Sequence[Notification]:
    stmt = select(Notification).where(Notification.user_id == user_id)

    if unread_only:
        stmt = stmt.where(Notification.is_read == False)

    stmt = stmt.order_by(Notification.created_at.desc()).limit(limit)

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_unread_notifications_count(
    session: AsyncSession,
    user_id: int,
) -> int:
    stmt = select(Notification).where(
        and_(Notification.user_id == user_id, Notification.is_read == False)
    )
    result = await session.execute(stmt)
    return len(result.scalars().all())


async def mark_notification_as_read(
    session: AsyncSession,
    notification_id: int,
) -> Notification | None:
    notification = await session.get(Notification, notification_id)
    if notification:
        notification.is_read = True
        await session.commit()
        await session.refresh(notification)
    return notification


async def mark_all_as_read(
    session: AsyncSession,
    user_id: int,
) -> None:
    stmt = select(Notification).where(
        and_(Notification.user_id == user_id, Notification.is_read == False)
    )
    result = await session.execute(stmt)
    notifications = result.scalars().all()

    for notification in notifications:
        notification.is_read = True

    if notifications:
        await session.commit()


async def delete_notification(
    session: AsyncSession,
    notification: Notification,
) -> None:
    await session.delete(notification)
    await session.commit()
