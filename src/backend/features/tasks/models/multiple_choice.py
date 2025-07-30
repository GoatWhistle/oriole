from sqlalchemy import ForeignKey, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from features.tasks.models import BaseTask
from features.tasks.schemas import MultipleChoiceTaskRead
from shared.enums import TaskTypeEnum


class MultipleChoiceTask(BaseTask):
    __tablename__ = "multiple_choice"
    __mapper_args__ = {"polymorphic_identity": TaskTypeEnum.MULTIPLE_CHOICE.value}

    id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    correct_answer: Mapped[list] = mapped_column(ARRAY(String))

    def get_validation_schema(self) -> MultipleChoiceTaskRead:
        return MultipleChoiceTaskRead.model_validate(self)
