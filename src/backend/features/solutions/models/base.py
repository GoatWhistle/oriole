from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.solutions.schemas import BaseSolutionRead
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

    is_correct: Mapped[bool] = mapped_column(default=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )

    @abstractmethod
    def get_validation_schema(self) -> BaseSolutionRead:
        return BaseSolutionRead.model_validate(self)
