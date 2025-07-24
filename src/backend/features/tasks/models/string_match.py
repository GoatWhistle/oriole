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

    compare_as_number: Mapped[bool] = mapped_column(default=False)
    is_case_sensitive: Mapped[bool | None] = mapped_column(default=None)
    normalize_whitespace: Mapped[bool | None] = mapped_column(default=None)

    def get_validation_schema(self) -> StringMatchTaskRead:
        return StringMatchTaskRead.model_validate(self)
