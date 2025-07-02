from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin

if TYPE_CHECKING:
    from features.users.models import UserProfile
    from features.groups.models import Group
    from features.solutions.models import BaseSolution
    from features import Chat
    from features import ChatAccountAssociation
    from features import Message


class Account(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    user_profile: Mapped["UserProfile"] = relationship(back_populates="accounts")

    role: Mapped[int] = mapped_column()

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="accounts")

    done_tasks: Mapped[list["BaseSolution"]] = relationship(back_populates="account")

    messages: Mapped[List["Message"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )

    chat_links: Mapped[List["ChatAccountAssociation"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )

    chats: Mapped[List["Chat"]] = relationship(
        secondary="chat_account_association", back_populates="accounts", viewonly=True
    )
