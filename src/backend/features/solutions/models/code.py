from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from features.solutions.models import BaseSolution
from features.solutions.schemas.code import CodeSolutionRead
from shared.enums import TaskTypeEnum, SolutionStatusEnum


class CodeSolution(BaseSolution):
    __tablename__ = "code_solutions"
    __mapper_args__ = {
        "polymorphic_identity": TaskTypeEnum.CODE,
    }
    id: Mapped[int] = mapped_column(
        ForeignKey("solutions.id", ondelete="CASCADE"), primary_key=True
    )
    code: Mapped[str] = mapped_column(default="")
    status: Mapped[str] = mapped_column(
        String, nullable=False, server_default=SolutionStatusEnum.SUBMITTING.value
    )

    def get_validation_schema(self) -> CodeSolutionRead:
        return CodeSolutionRead.model_validate(self)
