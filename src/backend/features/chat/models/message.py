from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database import Base


if TYPE_CHECKING:
    from features import Chat
    from features import Account


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chat.id", ondelete="CASCADE"), nullable=False
    )
    reply_to: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id"), nullable=True
    )
    reply_to_message: Mapped["Message"] = relationship("Message", remote_side=[id])
    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    account: Mapped["Account"] = relationship(back_populates="messages")
