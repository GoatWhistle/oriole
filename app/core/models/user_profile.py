from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .user_group_association import user_group_association_table

if TYPE_CHECKING:
    from .group import Group
    from .assignment import Assignment
    from .user import User
    from .task import Task


class UserProfile(Base):

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    user: Mapped["User"] = relationship(back_populates="profile")

    name: Mapped[str] = mapped_column(String(31), index=True)
    surname: Mapped[str] = mapped_column(String(31), index=True)
    patronymic: Mapped[str] = mapped_column(String(63), index=True)

    groups: Mapped[list[Optional["Group"]]] = relationship(
        secondary=user_group_association_table,
        back_populates="users",
    )

    admin_groups: Mapped[list[Optional["Group"]]] = relationship(back_populates="admin")

    admin_assignments: Mapped[list[Optional["Assignment"]]] = relationship(
        back_populates="admin"
    )
    done_tasks: Mapped[list[Optional["Task"]]] = relationship(back_populates="user")
