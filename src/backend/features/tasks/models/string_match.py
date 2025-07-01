from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from features.tasks.models import BaseTask
from features.tasks.schemas import StringMatchTaskModel
from shared.enums import TaskTypeEnum


class StringMatchTask(BaseTask):
    __mapper_args__ = {
        "polymorphic_identity": TaskTypeEnum.STRING_MATCH,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )

    is_case_sensitive: Mapped[bool] = mapped_column(default=True)
    normalize_whitespace: Mapped[bool] = mapped_column(default=False)
    standardize_numeric_punctuation: Mapped[bool] = mapped_column(default=False)
    ignore_leading_zeros_in_numbers: Mapped[bool] = mapped_column(default=False)

    def get_validation_schema(self) -> StringMatchTaskModel: ...
