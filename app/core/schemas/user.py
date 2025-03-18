from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

from .group import GroupBase
from .task import TaskRead


class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=32)]
    surname: Annotated[str, Field(max_length=32)]
    father_name: Annotated[str | None, Field(max_length=32)]

    email: Annotated[EmailStr, Field(max_length=50)]
    password: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    groups: list[GroupBase | None]
    admin_groups: list[GroupBase | None]
    admin_tasks: list[TaskRead | None]
