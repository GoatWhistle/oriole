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
    from .user_profile import UserProfile


class Task(Base, IdIntPkMixin):
    name: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column()
    correct_answer: Mapped[str] = mapped_column()

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="tasks")

    admin_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    admin: Mapped["UserProfile"] = relationship(back_populates="admin_tasks")
