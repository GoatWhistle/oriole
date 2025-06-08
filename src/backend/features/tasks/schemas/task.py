from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

from utils import get_number_one_bit_less as get_num_opt


class TaskBase(BaseModel):
    title: Annotated[str, Field(max_length=get_num_opt(100))]
    description: Annotated[str, Field(max_length=get_num_opt(200))]


class TaskCreate(TaskBase):
    module_id: int
    correct_answer: str

    max_attempts: int

    start_datetime: datetime
    end_datetime: datetime


class TaskReadPartial(TaskBase):
    id: int
    is_correct: bool

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskRead(TaskReadPartial):
    module_id: int
    group_id: int

    user_answer: str
    user_attempts: int

    max_attempts: int

    start_datetime: datetime
    end_datetime: datetime


class TaskUpdate(TaskBase):
    correct_answer: str
    max_attempts: int

    start_datetime: datetime
    end_datetime: datetime


class TaskUpdatePartial(TaskBase):
    title: Annotated[Optional[str], Field(max_length=get_num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=get_num_opt(200))] = None

    correct_answer: Optional[str] = None
    max_attempts: Optional[int] = None

    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
