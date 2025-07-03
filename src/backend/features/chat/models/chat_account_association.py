from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin

if TYPE_CHECKING:
    from features import Chat
    from features import Account


class ChatAccountAssociation(Base, IdIntPkMixin):
    __tablename__ = "chat_account_association"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"))
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    chat: Mapped["Chat"] = relationship(back_populates="account_links")
    account: Mapped["Account"] = relationship(back_populates="chat_links")
