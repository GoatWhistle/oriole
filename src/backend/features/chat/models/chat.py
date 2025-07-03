from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


if TYPE_CHECKING:
    from features import Group
    from features import Message
    from features import Account
    from features import ChatAccountAssociation


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)

    group: Mapped["Group"] = relationship("Group", back_populates="chat")
    creator: Mapped["Account"] = relationship("Account", back_populates="created_chats")

    messages: Mapped[List["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )

    account_links: Mapped[List["ChatAccountAssociation"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )

    accounts: Mapped[List["Account"]] = relationship(
        secondary="chat_account_association", back_populates="chats", viewonly=True
    )
