from typing import TYPE_CHECKING

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from utils.number_optimizer import get_number_one_bit_less as num_opt

if TYPE_CHECKING:
    from .assignment import Assignment
    from .account import Account
    from .group_invite import GroupInvite


class Group(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(num_opt(100)))
    description: Mapped[str] = mapped_column(String(num_opt(200)))

    accounts: Mapped[list["Account"]] = relationship(back_populates="group")
    assignments: Mapped[list["Assignment"]] = relationship(back_populates="group")
    invites: Mapped[list["GroupInvite"]] = relationship(back_populates="group")
