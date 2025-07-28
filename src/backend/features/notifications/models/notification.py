from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from shared.enums import NotificationTypeEnum

if TYPE_CHECKING:
    from features.users.models import UserProfile


class Notification(Base, IdIntPkMixin):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    title: Mapped[str] = mapped_column(String(100))
    message: Mapped[str] = mapped_column(String(500))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    related_entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone("UTC", func.now())
    )

    user: Mapped["UserProfile"] = relationship(back_populates="notifications")

    __mapper_args__ = {
        "polymorphic_identity": NotificationTypeEnum.BASE.value,
        "polymorphic_on": notification_type,
    }