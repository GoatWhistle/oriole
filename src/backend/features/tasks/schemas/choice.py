from pydantic import Field

from features.solutions.schemas import MultipleChoiceSolutionRead
from features.tasks.schemas import (
    BaseTaskModel,
    BaseTaskRead,
    BaseTaskCreate,
    BaseTaskUpdate,
    BaseTaskReadWithCorrectness,
    BaseTaskReadWithSolutions,
)


class MultipleChoiceTaskBase(BaseTaskModel):
    pass


class MultipleChoiceTaskCreate(MultipleChoiceTaskBase, BaseTaskCreate):
    correct_answer: list


class MultipleChoiceTaskRead(MultipleChoiceTaskBase, BaseTaskRead):
    def to_with_correctness(
        self,
        is_correct: bool,
        user_attempts: int,
    ) -> "MultipleChoiceTaskReadWithCorrectness":
        return MultipleChoiceTaskReadWithCorrectness(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts=user_attempts,
        )

    def to_with_solutions(
        self,
        is_correct: bool,
        user_attempts: int,
        solutions: list[MultipleChoiceSolutionRead],
    ) -> "MultipleChoiceTaskReadWithSolutions":
        return MultipleChoiceTaskReadWithSolutions(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts=user_attempts,
            solutions=solutions,
        )


class MultipleChoiceTaskReadWithCorrectness(
    MultipleChoiceTaskRead, BaseTaskReadWithCorrectness
):
    pass


class MultipleChoiceTaskReadWithSolutions(
    MultipleChoiceTaskReadWithCorrectness, BaseTaskReadWithSolutions
):
    solutions: list[MultipleChoiceSolutionRead]


class MultipleChoiceTaskUpdate(BaseTaskUpdate):
    correct_answer: list | None
