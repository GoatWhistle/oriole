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
    compare_as_number: bool = False
    is_case_sensitive: bool | None = None
    normalize_whitespace: bool | None = None


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


class StringMatchTaskUpdate(BaseTaskUpdate):
    correct_answer: str | None = Field(default=None, max_length=300)

    compare_as_number: bool | None = None
    is_case_sensitive: bool | None = None
    normalize_whitespace: bool | None = None
