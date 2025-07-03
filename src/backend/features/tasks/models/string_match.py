from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from features.tasks.models import BaseTask
from features.tasks.schemas import StringMatchTaskRead
from shared.enums import TaskTypeEnum


class StringMatchTask(BaseTask):
    __tablename__ = "string_match_tasks"
    __mapper_args__ = {"polymorphic_identity": TaskTypeEnum.STRING_MATCH.value}

    id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    correct_answer: Mapped[str] = mapped_column(String(300))

    is_case_sensitive: Mapped[bool] = mapped_column(default=True)
    normalize_whitespace: Mapped[bool] = mapped_column(default=False)
    standardize_numeric_punctuation: Mapped[bool] = mapped_column(default=False)
    ignore_leading_zeros_in_numbers: Mapped[bool] = mapped_column(default=False)

    def get_validation_schema(
        self,
        is_correct: bool = False,
        user_attempts: int = 0,
    ) -> StringMatchTaskRead:
        data = StringMatchTaskRead.model_validate(self)
        return data.model_copy(
            update={"is_correct": is_correct, "user_attempts": user_attempts}
        )
