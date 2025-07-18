from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.accounts.schemas import AccountRead

if TYPE_CHECKING:
    from features.users.models import UserProfile
    from features.spaces.models import Space
    from features.solutions.models import BaseSolution
    from features.modules.models import Module
    from features.tasks.models import BaseTask
    from features import Chat
    from features import ChatAccountAssociation
    from features import Message


class Account(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    user_profile: Mapped["UserProfile"] = relationship(back_populates="accounts")

    role: Mapped[int] = mapped_column()

    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id", ondelete="CASCADE"))
    space: Mapped["Space"] = relationship(back_populates="accounts")

    created_modules: Mapped[list["Module"]] = relationship(back_populates="creator")
    created_tasks: Mapped[list["BaseTask"]] = relationship(back_populates="creator")
    created_solutions: Mapped[list["BaseSolution"]] = relationship(
        back_populates="creator"
    )

    messages: Mapped[List["Message"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )
    chat_links: Mapped[List["ChatAccountAssociation"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )
    chats: Mapped[List["Chat"]] = relationship(
        secondary="chat_account_association", back_populates="accounts", viewonly=True
    )

    def get_validation_schema(self) -> AccountRead:
        return AccountRead.model_validate(self)
