from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, IdIntPkMixin

if TYPE_CHECKING:
    from features.accounts.models import Account
    from features.tasks.models import BaseTask


class AccountTaskProgress(Base, IdIntPkMixin):
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

    is_correct: Mapped[bool] = mapped_column(default=False)
    user_attempts: Mapped[int] = mapped_column(Integer, default=0)

    account: Mapped["Account"] = relationship(back_populates="task_progresses")
    task: Mapped["BaseTask"] = relationship(back_populates="account_progresses")
