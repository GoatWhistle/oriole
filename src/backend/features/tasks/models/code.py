from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from features.tasks.models import BaseTask
from features.tasks.schemas import CodeTaskRead
from shared.enums import TaskTypeEnum

if TYPE_CHECKING:
    from features.tasks.models.test import Test


class CodeTask(BaseTask):
    __tablename__ = "code_tasks"
    __mapper_args__ = {"polymorphic_identity": TaskTypeEnum.CODE.value}

    id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    time_limit: Mapped[int] = mapped_column(nullable=False)
    memory_limit: Mapped[int] = mapped_column(nullable=False)

    tests: Mapped[list["Test"]] = relationship(back_populates="task")

    def get_validation_schema(
        self,
        is_correct: bool = False,
        user_attempts: int = 0,
    ) -> CodeTaskRead:
        data = CodeTaskRead.model_validate(self)
        return data.model_copy(
            update={"is_correct": is_correct, "user_attempts": user_attempts}
        )
