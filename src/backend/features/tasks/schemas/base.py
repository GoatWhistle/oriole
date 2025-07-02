from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BaseTaskModel(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=500)

    manual_grading: bool
    max_attempts: int

    start_datetime: datetime
    end_datetime: datetime


class BaseTaskCreate(BaseTaskModel):
    module_id: int


class BaseTaskRead(BaseTaskModel):
    id: int

    is_active: bool

    module_id: int
    space_id: int

    is_correct: bool
    user_attempts: int

    model_config = ConfigDict(from_attributes=True)


class BaseTaskUpdatePartial(BaseTaskModel):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    max_attempts: str | None = None
    manual_grading: bool | None = None

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
