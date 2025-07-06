from features.solutions.schemas import CodeSolutionRead
from features.tasks.schemas import (
    BaseTaskModel,
    BaseTaskRead,
    BaseTaskCreate,
    BaseTaskUpdate,
    BaseTaskReadWithCorrectness,
    BaseTaskReadWithSolutions,
)


class CodeTaskBase(BaseTaskModel):
    time_limit: int
    memory_limit: int


class CodeTaskCreate(CodeTaskBase, BaseTaskCreate):
    pass


class CodeTaskRead(CodeTaskBase, BaseTaskRead):
    def to_with_correctness(
        self,
        is_correct: bool,
        user_attempts: int,
    ) -> "CodeTaskReadWithCorrectness":
        return CodeTaskReadWithCorrectness(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts=user_attempts,
        )

    def to_with_solutions(
        self,
        is_correct: bool,
        user_attempts: int,
        solutions: list[CodeSolutionRead],
    ) -> "CodeTaskReadWithSolutions":
        return CodeTaskReadWithSolutions(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts=user_attempts,
            solutions=solutions,
        )


class CodeTaskReadWithCorrectness(CodeTaskRead, BaseTaskReadWithCorrectness):
    pass


class CodeTaskReadWithSolutions(CodeTaskRead, BaseTaskReadWithSolutions):
    solutions: list[CodeSolutionRead]


class CodeTaskUpdate(BaseTaskUpdate):
    time_limit: int | None = None
    memory_limit: int | None = None
