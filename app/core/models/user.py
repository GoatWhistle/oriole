from typing import TYPE_CHECKING, Optional

from .base import Base

from .user_group_association import user_group_association_table

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from pydantic import EmailStr

if TYPE_CHECKING:
    from .group import Group
    from .task import Task


class User(Base):
    name: Mapped[str] = mapped_column(String(32))
    surname: Mapped[str] = mapped_column(String(32))
    father_name: Mapped[str | None] = mapped_column(String(32))

    email: Mapped[EmailStr] = mapped_column(String(50), unique=True)

    password: Mapped[str] = mapped_column()

    groups: Mapped[list[Optional["Group"]]] = relationship(
        secondary=user_group_association_table,
        back_populates="users",
    )

    admin_groups: Mapped[list[Optional["Group"]]] = relationship(back_populates="admin")

    admin_tasks: Mapped[list[Optional["Task"]]] = relationship(back_populates="admin")
