from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from features.tasks.schemas import BaseTaskRead
from shared.enums import TaskTypeEnum

if TYPE_CHECKING:
    from features.modules.models import Module
    from features.solutions.models import BaseSolution


class BaseTask(Base, IdIntPkMixin):
    __tablename__ = "tasks"

    task_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    __mapper_args__ = {
        "polymorphic_identity": TaskTypeEnum.BASE.value,
        "polymorphic_on": task_type,
        "with_polymorphic": "*",
    }

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))

    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="tasks")

    solutions: Mapped[List["BaseSolution"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )

    can_attempt: Mapped[bool] = mapped_column(default=False)
    manual_grading: Mapped[bool] = mapped_column(default=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=0)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=False)

    @property
    def space_id(self) -> int:
        return self.module.space_id

    @abstractmethod
    def get_validation_schema(
        self,
        is_correct: bool = False,
        user_attempts: int = 0,
    ) -> BaseTaskRead:
        data = BaseTaskRead.model_validate(self)
        return data.model_copy(
            update={"is_correct": is_correct, "user_attempts": user_attempts}
        )
