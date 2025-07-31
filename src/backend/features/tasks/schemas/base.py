from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from features.solutions.schemas import BaseSolutionRead


class BaseTaskModel(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=500)

    can_attempt: bool = False
    max_attempts: int = 0

    start_datetime: datetime
    end_datetime: datetime


class BaseTaskCreate(BaseTaskModel):
    module_id: int


class BaseTaskRead(BaseTaskModel):
    id: int

    is_active: bool

    creator_id: int
    module_id: int
    space_id: int

    model_config = ConfigDict(from_attributes=True)

    def to_with_progress(
        self,
        is_correct: bool,
        user_attempts_count: int,
    ) -> "BaseTaskReadWithProgress":
        return BaseTaskReadWithProgress(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts_count=user_attempts_count,
        )

    def to_with_solutions(
        self,
        is_correct: bool,
        user_attempts_count: int,
        solutions: list[BaseSolutionRead],
    ) -> "BaseTaskReadWithSolutions":
        return BaseTaskReadWithSolutions(
            **self.model_dump(),
            is_correct=is_correct,
            user_attempts_count=user_attempts_count,
            solutions=solutions,
        )


class BaseTaskReadWithProgress(BaseTaskRead):
    is_correct: bool
    user_attempts_count: int


class BaseTaskReadWithSolutions(BaseTaskReadWithProgress):
    solutions: list[BaseSolutionRead]


class BaseTaskUpdate(BaseTaskModel):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    can_attempt: bool | None = None
    max_attempts: int | None = None

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
