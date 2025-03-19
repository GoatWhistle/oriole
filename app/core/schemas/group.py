from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

from .user import UserRead
from .task import TaskRead


class GroupBase(BaseModel):
    title: Annotated[str, Field(max_length=64)]
    description: Annotated[str, Field(max_length=200)]
    admin: UserRead
    admin_id: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupCreate):
    pass


class GroupUpdatePartial(GroupCreate):
    title: Annotated[Optional[str], Field(max_length=64)] = None
    description: Annotated[Optional[str], Field(max_length=200)] = None
    admin: Optional[UserRead] = None
    admin_id: Optional[int] = None


class GroupRead(GroupBase):
    id: int
    users: list[UserRead] = []
    tasks: list[TaskRead] = []

    model_config = ConfigDict(from_attributes=True)
