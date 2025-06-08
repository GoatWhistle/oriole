from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from utils import get_number_one_bit_less as get_num_opt

if TYPE_CHECKING:
    from features.modules.models import Module
    from .user_reply import UserReply


class Task(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(get_num_opt(100)))
    description: Mapped[str] = mapped_column(String(get_num_opt(200)))
    correct_answer: Mapped[str] = mapped_column()

    module_id: Mapped[int] = mapped_column(ForeignKey("module.id"))
    module: Mapped["Module"] = relationship(back_populates="tasks")

    user_replies: Mapped[list["UserReply"]] = relationship(back_populates="task")

    max_attempts: Mapped[int] = mapped_column(Integer, default=0)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=False)
