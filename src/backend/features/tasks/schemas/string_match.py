from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from features.tasks.schemas import BaseTaskModel
from utils import get_number_one_bit_less as get_num_opt


class StringMatchTaskModel(BaseTaskModel):
    pass


class TaskBase(BaseModel):
    title: str = Field(max_length=get_num_opt(100))
    description: str = Field(max_length=get_num_opt(200))

    start_datetime: datetime
    end_datetime: datetime

    max_attempts: int


class TaskCreate(TaskBase):
    module_id: int
    correct_answer: str


class TaskRead(TaskBase):
    id: int

    is_correct: bool
    is_active: bool

    module_id: int
    group_id: int

    user_answer: str
    user_attempts: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskUpdate(TaskBase):
    correct_answer: str


class TaskUpdatePartial(TaskUpdate):
    title: str | None = Field(default=None, max_length=get_num_opt(100))
    description: str | None = Field(default=None, max_length=get_num_opt(200))

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None

    max_attempts: str | None = None
    correct_answer: str | None = None


class TaskReadWithoutReplies(TaskBase):
    id: int
    is_active: bool
    is_correct: bool
    module_id: int
    group_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
