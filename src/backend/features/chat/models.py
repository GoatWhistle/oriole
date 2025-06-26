from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from database import Base

if TYPE_CHECKING:
    from ..groups.models import Group
    from ..users.models import User

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    group: Mapped["Group"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages")

