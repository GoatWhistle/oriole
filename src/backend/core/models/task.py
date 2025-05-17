from datetime import datetime
from typing import TYPE_CHECKING

from core.models.assignment import Assignment
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from utils.number_optimizer import get_number_one_bit_less as num_opt

if TYPE_CHECKING:
    from .assignment import Assignment
    from .user_reply import UserReply


class Task(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(num_opt(100)))
    description: Mapped[str] = mapped_column(String(num_opt(200)))
    correct_answer: Mapped[str] = mapped_column()

    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    assignment: Mapped["Assignment"] = relationship(back_populates="tasks")

    user_replys: Mapped[list["UserReply"]] = relationship(back_populates="task")

    max_attempts: Mapped[int] = mapped_column(Integer, default=0)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=False)
