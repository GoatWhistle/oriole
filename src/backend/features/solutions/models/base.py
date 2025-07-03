from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import String, ForeignKey, Integer, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from features.solutions.schemas import BaseSolutionModel
from shared.enums import TaskTypeEnum

if TYPE_CHECKING:
    from features.accounts.models import Account
    from features.tasks.models import BaseTask


class BaseSolution(Base, IdIntPkMixin):
    __tablename__ = "solutions"

    task_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    __mapper_args__ = {
        "polymorphic_identity": TaskTypeEnum.BASE,
        "polymorphic_on": task_type,
        "with_polymorphic": "*",
    }

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

    account: Mapped["Account"] = relationship(back_populates="done_tasks")
    task: Mapped["BaseTask"] = relationship(back_populates="solutions")

    user_answer: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    is_correct: Mapped[bool] = mapped_column(nullable=False, default=False)
    user_attempts: Mapped[int] = mapped_column(Integer, default=0)

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )

    @abstractmethod
    def get_validation_schema(self) -> BaseSolutionModel: ...
