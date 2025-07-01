from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, List, Dict, Any

from sqlalchemy import String, ForeignKey, Integer, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from features.tasks.schemas import BaseTaskModel
from shared.enums import TaskTypeEnum

if TYPE_CHECKING:
    from features.modules.models import Module
    from features.solutions.models import BaseSolution


class BaseTask(Base, IdIntPkMixin, ABC):
    __tablename__ = "tasks"

    task_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    __mapper_args__ = {
        "polymorphic_identity": TaskTypeEnum.BASE,
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

    correct_answer: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    manual_grading: Mapped[bool] = mapped_column(default=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=0)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=False)

    @abstractmethod
    def get_validation_schema(self) -> BaseTaskModel: ...
