from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import BaseTask

from datetime import timedelta
from features.notifications.services.notification import send_notification, was_notification_sent
from shared.enums import NotificationTypeEnum


async def check_deadline_notifications(
        session: AsyncSession,
        task: BaseTask,
        time_left: timedelta
):
    minutes_left = time_left.total_seconds() / 60

    if 60*24 <= minutes_left < 60*24+1:
        if not await was_notification_sent(session, task.id, NotificationTypeEnum.DEADLINE_24H):
            await send_deadline_notification(
                session, task,
                hours=24,
                notification_type=NotificationTypeEnum.DEADLINE_24H
            )

    elif 60 <= minutes_left < 61:
        if not await was_notification_sent(session, task.id, NotificationTypeEnum.DEADLINE_1H):
            await send_deadline_notification(
                session, task,
                hours=1,
                notification_type=NotificationTypeEnum.DEADLINE_1H
            )

    elif minutes_left < 0:
        if not await was_notification_sent(session, task.id, NotificationTypeEnum.DEADLINE_OVERDUE):
            await send_deadline_notification(
                session, task,
                hours=0,
                notification_type=NotificationTypeEnum.DEADLINE_OVERDUE
            )


async def send_deadline_notification(
        session: AsyncSession,
        task: BaseTask,
        hours: int,
        notification_type: NotificationTypeEnum
):
    message = (
        f"До дедлайна задачи «{task.title}» осталось {hours} часов" if hours > 0
        else f"Задача «{task.title}» просрочена!"
    )

    await send_notification(
        session=session,
        user_id=task.creator_id,
        title="Напоминание о дедлайне",
        message=message,
        notification_type=notification_type,
        entity_id=task.id
    )
