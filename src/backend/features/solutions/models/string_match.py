from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from features.solutions.models import BaseSolution
from features.solutions.schemas.string_match import StringMatchSolutionModel
from shared.enums import TaskTypeEnum


class StringMatchSolution(BaseSolution):
    __mapper_args__ = {
        "polymorphic_identity": TaskTypeEnum.STRING_MATCH,
    }
    id: Mapped[int] = mapped_column(
        ForeignKey("solutions.id", ondelete="CASCADE"), primary_key=True
    )

    def get_validation_schema(self) -> StringMatchSolutionModel: ...
