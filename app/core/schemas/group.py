from pydantic import BaseModel, Field
from typing import Annotated

from .user import UserRead
from .task import TaskRead


class GroupBase(BaseModel):
    title: Annotated[str, Field(max_length=64)]
    admin: UserRead
    admin_id: int


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: int
    users: list[UserRead] = []
    tasks: list[TaskRead] = []
