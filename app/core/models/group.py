from typing import TYPE_CHECKING, Optional

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from .assignment import Assignment
    from .account import Account


class Group(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(63))
    description: Mapped[str] = mapped_column(String(200))

    accounts: Mapped[list["Account"]] = relationship(back_populates="group")

    assignments: Mapped[list[Optional["Assignment"]]] = relationship(
        back_populates="group"
    )
