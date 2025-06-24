from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from src.backend.database import Base

if TYPE_CHECKING:
    from ..groups.models import Group
    from ..users.models import User

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages")
