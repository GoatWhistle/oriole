from features.solutions.schemas import MultipleChoiceSolutionRead
from features.tasks.schemas import (
    BaseTaskCreate,
    BaseTaskModel,
    BaseTaskRead,
    BaseTaskReadWithProgress,
    BaseTaskReadWithSolutions,
    BaseTaskUpdate,
)


class MultipleChoiceTaskBase(BaseTaskModel):
    pass


class MultipleChoiceTaskCreate(MultipleChoiceTaskBase, BaseTaskCreate):
    correct_answer: list[str]


class MultipleChoiceTaskRead(MultipleChoiceTaskBase, BaseTaskRead):
    def to_with_progress(
        self,
        is_correct: bool,
        user_attempts: int,
    ) -> "MultipleChoiceTaskReadWithProgress":
        return MultipleChoiceTaskReadWithProgress(
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


class MultipleChoiceTaskReadWithProgress(
    MultipleChoiceTaskRead, BaseTaskReadWithProgress
):
    pass


class MultipleChoiceTaskReadWithSolutions(
    MultipleChoiceTaskReadWithProgress, BaseTaskReadWithSolutions
):
    solutions: list[MultipleChoiceSolutionRead]


class MultipleChoiceTaskUpdate(BaseTaskUpdate):
    correct_answer: list | None
