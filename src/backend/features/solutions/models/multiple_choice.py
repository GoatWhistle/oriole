from sqlalchemy import ForeignKey, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from features.solutions.models import BaseSolution
from features.solutions.schemas import MultipleChoiceSolutionRead
from shared.enums import TaskTypeEnum


class MultipleChoiceSolution(BaseSolution):
    __tablename__ = "multiple_choice_solutions"
    __mapper_args__ = {"polymorphic_identity": TaskTypeEnum.MULTIPLE_CHOICE}

    id: Mapped[int] = mapped_column(
        ForeignKey("solutions.id", ondelete="CASCADE"), primary_key=True
    )

    user_answer: Mapped[list] = mapped_column(ARRAY(String))

    def get_validation_schema(self) -> MultipleChoiceSolutionRead:
        return MultipleChoiceSolutionRead.model_validate(self)
