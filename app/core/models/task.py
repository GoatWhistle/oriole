from typing import TYPE_CHECKING

from core.models.assignment import Assignment
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
    from .assignment import Assignment


class Task(Base, IdIntPkMixin):
    name: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column()
    correct_answer: Mapped[str] = mapped_column()

    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    assignment: Mapped["Assignment"] = relationship(back_populates="tasks")

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    user: Mapped["UserProfile"] = relationship(back_populates="done_tasks")
