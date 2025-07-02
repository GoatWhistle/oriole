from features.tasks.schemas import (
    BaseTaskModel,
    BaseTaskRead,
    BaseTaskCreate,
    BaseTaskUpdatePartial,
)


class StringMatchTaskBase(BaseTaskModel):
    is_case_sensitive: bool
    normalize_whitespace: bool
    standardize_numeric_punctuation: bool
    ignore_leading_zeros_in_numbers: bool


class StringMatchTaskCreate(StringMatchTaskBase, BaseTaskCreate):
    correct_answer: str


class StringMatchTaskRead(StringMatchTaskBase, BaseTaskRead):
    pass


class StringMatchTaskUpdate(StringMatchTaskBase):
    correct_answer: str


class StringMatchTaskUpdatePartial(StringMatchTaskUpdate, BaseTaskUpdatePartial):
    correct_answer: str | None = None

    is_case_sensitive: bool | None = None
    normalize_whitespace: bool | None = None
    standardize_numeric_punctuation: bool | None = None
    ignore_leading_zeros_in_numbers: bool | None = None
