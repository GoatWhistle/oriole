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
    def to_with_correctness(
        self,
        is_correct: bool,
        user_attempts: int,
    ) -> "StringMatchTaskReadWithCorrectness":
        return StringMatchTaskReadWithCorrectness(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts=user_attempts,
        )

    def to_with_solutions(
        self,
        is_correct: bool,
        user_attempts: int,
        solutions: list[StringMatchSolutionRead],
    ) -> "StringMatchTaskReadWithSolutions":
        return StringMatchTaskReadWithSolutions(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts=user_attempts,
            solutions=solutions,
        )


class StringMatchTaskReadWithCorrectness(
    StringMatchTaskRead, BaseTaskReadWithCorrectness
):
    pass


class StringMatchTaskReadWithSolutions(
    StringMatchTaskReadWithCorrectness, BaseTaskReadWithSolutions
):
    solutions: list[StringMatchSolutionRead]


class StringMatchTaskUpdate(StringMatchTaskBase, BaseTaskUpdate):
    correct_answer: str | None = Field(default=None, max_length=300)

    is_case_sensitive: bool | None = None
    normalize_whitespace: bool | None = None
    standardize_numeric_punctuation: bool | None = None
    ignore_leading_zeros_in_numbers: bool | None = None
