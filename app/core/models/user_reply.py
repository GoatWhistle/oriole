from typing import TYPE_CHECKING

from . import Task
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from utils.number_optimizer import get_number_one_bit_less as num_opt

if TYPE_CHECKING:
    from .account import Account


class UserReply(Base, IdIntPkMixin):
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship(back_populates="done_tasks")

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship(back_populates="user_replys")

    user_answer: Mapped[str] = mapped_column(String(num_opt(200)))
    is_correct: Mapped[bool] = mapped_column()

    user_attempts: Mapped[int] = mapped_column()
