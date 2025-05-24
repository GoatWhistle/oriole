from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional

from utils.number_optimizer import get_number_one_bit_less as num_opt


class TaskBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]


class TaskReadPartial(TaskBase):
    id: int
    is_correct: bool

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskRead(TaskReadPartial):
    user_answer: str
    user_attempts: int

    max_attempts: int

    start_datetime: int
    end_datetime: int


class TaskCreate(TaskBase):
    assignment_id: int
    correct_answer: str

    max_attempts: int

    start_datetime: int
    end_datetime: int


class TaskUpdate(TaskBase):
    correct_answer: str
    max_attempts: int

    start_datetime: int
    end_datetime: int


class TaskUpdatePartial(TaskBase):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None

    correct_answer: Optional[str] = None
    max_attempts: Optional[int] = None

    start_datetime: Optional[int] = None
    end_datetime: Optional[int] = None
