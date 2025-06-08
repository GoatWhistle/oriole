from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from utils import get_number_one_bit_less as get_num_opt

if TYPE_CHECKING:
    from groups.models import Group
    from tasks.models import Task
    from users.models import UserProfile


class Module(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(get_num_opt(100)))
    description: Mapped[str] = mapped_column(String(get_num_opt(200)))

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
