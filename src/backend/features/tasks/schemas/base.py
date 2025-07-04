from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from features.solutions.schemas import BaseSolutionRead


class BaseTaskModel(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=500)

    can_attempt: bool = False
    manual_grading: bool = False
    max_attempts: int = 0

    start_datetime: datetime
    end_datetime: datetime


class BaseTaskCreate(BaseTaskModel):
    module_id: int


class BaseTaskRead(BaseTaskModel):
    id: int

    is_active: bool

    module_id: int
    space_id: int

    model_config = ConfigDict(from_attributes=True)


class BaseTaskReadWithCorrectness(BaseTaskRead):
    is_correct: bool
    user_attempts: int


class BaseTaskReadWithSolutions(BaseTaskReadWithCorrectness):
    solutions: list[BaseSolutionRead]


class BaseTaskUpdate(BaseTaskModel):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    can_attempt: bool | None = None
    manual_grading: bool | None = None
    max_attempts: int | None = None

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
