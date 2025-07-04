from pydantic import Field

from features.solutions.schemas import StringMatchSolutionRead
from features.tasks.schemas import (
    BaseTaskModel,
    BaseTaskRead,
    BaseTaskCreate,
    BaseTaskUpdate,
    BaseTaskReadWithCorrectness,
    BaseTaskReadWithSolutions,
)


class StringMatchTaskBase(BaseTaskModel):
    is_case_sensitive: bool = True
    normalize_whitespace: bool = False
    standardize_numeric_punctuation: bool = False
    ignore_leading_zeros_in_numbers: bool = False


class StringMatchTaskCreate(StringMatchTaskBase, BaseTaskCreate):
    correct_answer: str = Field(max_length=300)


class StringMatchTaskRead(StringMatchTaskBase, BaseTaskRead):
    pass


class StringMatchTaskReadWithCorrectness(
    StringMatchTaskRead, BaseTaskReadWithCorrectness
):
    pass


class StringMatchTaskReadWithSolutions(
    StringMatchTaskReadWithCorrectness, BaseTaskReadWithSolutions
):
    solutions: list[StringMatchSolutionRead]


class StringMatchTaskUpdate(BaseTaskUpdate):
    correct_answer: str | None = Field(default=None, max_length=300)

    is_case_sensitive: bool | None = None
    normalize_whitespace: bool | None = None
    standardize_numeric_punctuation: bool | None = None
    ignore_leading_zeros_in_numbers: bool | None = None
