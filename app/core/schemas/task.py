from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional


class TaskBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    text: str
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
    name: Annotated[str, Field(max_length=100)] = None
    text: Optional[str] = None
    correct_answer: Optional[str] = None

    assignment_id: Optional[int] = None

    account_id: Optional[int] = None
