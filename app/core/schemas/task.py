from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional

from utils.number_optimizer import get_number_one_bit_less as num_opt


class TaskBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]

    correct_answer: str

    assignment_id: int
    account_id: int


class TaskRead(TaskBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None

    correct_answer: Optional[str] = None

    assignment_id: Optional[int] = None
    account_id: Optional[int] = None
