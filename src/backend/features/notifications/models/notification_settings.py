from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin

if TYPE_CHECKING:
    from features.notifications.models import Notification


class UserNotificationSettings(Base, IdIntPkMixin):
    __tablename__ = "user_notification_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))

    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    telegram_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    chat_notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    system_notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True) #base
    deadline_notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user_settings",
        cascade="all, delete-orphan",
        order_by="Notification.created_at.desc()"
    )
