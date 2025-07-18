from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from features.solutions.models import BaseSolution
from features.solutions.schemas import StringMatchSolutionRead
from shared.enums import TaskTypeEnum


class StringMatchSolution(BaseSolution):
    __tablename__ = "string_match_solutions"
    __mapper_args__ = {"polymorphic_identity": TaskTypeEnum.STRING_MATCH.value}

    id: Mapped[int] = mapped_column(
        ForeignKey("solutions.id", ondelete="CASCADE"), primary_key=True
    )

    user_answer: Mapped[str] = mapped_column(String(300))

    def get_validation_schema(self) -> StringMatchSolutionRead:
        return StringMatchSolutionRead.model_validate(self)
