from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin


if TYPE_CHECKING:
    from features import Group
    from features import Message
    from features import Account
    from features import ChatAccountAssociation


class Chat(Base, IdIntPkMixin):
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)

    group: Mapped["Group"] = relationship("Group", back_populates="chat")

    messages: Mapped[List["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )

    account_links: Mapped[List["ChatAccountAssociation"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )

    accounts: Mapped[List["Account"]] = relationship(
        secondary="chat_account_associations", back_populates="chat", viewonly=True
    )
