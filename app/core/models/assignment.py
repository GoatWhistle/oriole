from typing import TYPE_CHECKING

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from .group import Group
    from .task import Task
    from .user_profile import UserProfile


class Assignment(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column()
    is_contest: Mapped[bool] = mapped_column()

    admin_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    admin: Mapped["UserProfile"] = relationship(back_populates="admin_assignments")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="assignments")

    tasks: Mapped[list["Task"]] = relationship(back_populates="assignment")
