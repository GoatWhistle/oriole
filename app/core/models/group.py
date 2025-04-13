from typing import TYPE_CHECKING, Optional

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


class Group(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(num_opt(100)))
    description: Mapped[str] = mapped_column(String(num_opt(200)))

    accounts: Mapped[list["Account"]] = relationship(back_populates="group")
    assignments: Mapped[list[Optional["Assignment"]]] = relationship(
        back_populates="group"
    )
