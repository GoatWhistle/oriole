from datetime import datetime

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from utils.number_optimizer import get_number_one_bit_less as num_opt

if TYPE_CHECKING:
    from .group import Group
    from .task import Task
    from .user_profile import UserProfile


class Assignment(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(num_opt(100)))
    description: Mapped[str] = mapped_column(String(num_opt(200)))

    is_contest: Mapped[bool] = mapped_column()

    admin_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    admin: Mapped["UserProfile"] = relationship(back_populates="admin_assignments")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="assignments")

    tasks: Mapped[list["Task"]] = relationship(back_populates="assignment")
    tasks_count: Mapped[int] = mapped_column(Integer, default=0)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=False)
