from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base

if TYPE_CHECKING:
    from features import Chat
    from features import ChatAccountAssociation
    from features import Group
    from features import UserReply
    from features import UserProfile
    from features import Message


class Account(Base, IdIntPkMixin):
    __tablename__ = "account"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    role: Mapped[int] = mapped_column()

    user_profile: Mapped["UserProfile"] = relationship(back_populates="accounts")
    group: Mapped["Group"] = relationship(back_populates="accounts")
    done_tasks: Mapped[List["UserReply"]] = relationship(back_populates="account")

    messages: Mapped[List["Message"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )

    chat_links: Mapped[List["ChatAccountAssociation"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )

    chats: Mapped[List["Chat"]] = relationship(
        secondary="chat_account_association", back_populates="accounts", viewonly=True
    )

    created_chats: Mapped[List["Chat"]] = relationship(
        "Chat", back_populates="creator", foreign_keys="[Chat.creator_id]"
    )
