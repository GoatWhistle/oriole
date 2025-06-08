from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from utils import get_number_one_bit_less as num_opt

if TYPE_CHECKING:
    from groups.models import Account
    from .task import Task


class UserReply(Base, IdIntPkMixin):
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship(back_populates="done_tasks")

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship(back_populates="user_replies")

    user_answer: Mapped[str] = mapped_column(String(num_opt(200)))
    is_correct: Mapped[bool] = mapped_column()

    user_attempts: Mapped[int] = mapped_column(Integer, default=0)
