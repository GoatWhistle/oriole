from typing import TYPE_CHECKING, Optional

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from .user_group_association import user_group_association_table

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from .user import User
    from .task import Task


class Group(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(64))

    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin: Mapped["User"] = relationship(back_populates="admin_groups")

    users: Mapped[list["User"]] = relationship(
        secondary=user_group_association_table,
        back_populates="groups",
    )  # many to many

    tasks: Mapped[list[Optional["Task"]]] = relationship(back_populates="group")
