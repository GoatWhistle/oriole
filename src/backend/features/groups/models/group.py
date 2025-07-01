from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from utils import get_number_one_bit_less as get_num_opt

if TYPE_CHECKING:
    from features import Module
    from features import Account, GroupInvite
    from features import Chat

class Group(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(get_num_opt(100)))
    description: Mapped[str] = mapped_column(String(get_num_opt(200)))

    accounts: Mapped[list["Account"]] = relationship(back_populates="group")
    modules: Mapped[list["Module"]] = relationship(back_populates="group")
    invites: Mapped[list["GroupInvite"]] = relationship(back_populates="group")
    chat: Mapped["Chat"] = relationship(
        "Chat", back_populates="group", uselist=False, cascade="all, delete-orphan"
    )
