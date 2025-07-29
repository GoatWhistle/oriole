from typing import Sequence

from features.notifications.models import Notification
from features.notifications.schemas import NotificationRead


def build_notification_read_list(
    notifications: Sequence[Notification],
) -> list[NotificationRead]:
    return [NotificationRead.model_validate(n) for n in notifications]
