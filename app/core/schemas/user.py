from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from fastapi_users import schemas

from .group import GroupBase
from .task import TaskRead
from core.types.user_id import UserIdType


# TODO: обратить внимание
class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=32)]
    surname: Annotated[str, Field(max_length=32)]
    father_name: Annotated[str | None, Field(max_length=32)]

    email: Annotated[EmailStr, Field(max_length=50)]
    password: str


class UserRead(schemas.BaseUser[UserIdType]):
    id: int
    groups: list[GroupBase | None]
    admin_groups: list[GroupBase | None]
    admin_tasks: list[TaskRead | None]


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRegisteredNotification(BaseModel):
    user: UserRead
    ts: int
