from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

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

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    name: Annotated[Optional[str], Field(max_length=100)]
    text: Optional[str]
    correct_answer: Optional[str]

    group: Optional[GroupRead]
    group_id: Optional[int]

    admin: Optional[UserRead]
    admin_id: Optional[int]
