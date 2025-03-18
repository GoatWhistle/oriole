from pydantic import BaseModel, Field
from typing import Annotated

from .group import GroupRead
from .user import UserRead


class TaskBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    text: str
    correct_answer: str

    group: GroupRead
    group_id: int

    admin: UserRead
    admin_id: int


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
