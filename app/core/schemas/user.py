from pydantic import BaseModel, EmailStr, Field, constr
from typing import Annotated, Optional
from fastapi_users import schemas

from .group import GroupBase
from .task import TaskRead
from core.types.user_id import UserIdType


class UserProfileDataBase(BaseModel):
    name: Annotated[constr(max_length=31), Field(example="Иван")]
    surname: Annotated[constr(max_length=31), Field(example="Петров")]
    patronymic: Annotated[
        Optional[constr(max_length=63)], Field(example="Сергеевич")
    ] = None
    email: Annotated[EmailStr, Field(example="user@example.com")]


class UserCreate(schemas.BaseUserCreate, UserProfileDataBase):
    pass


class UserPersonalDataUpdate(BaseModel):
    name: Annotated[Optional[str], Field(max_length=31)] = None
    surname: Annotated[Optional[str], Field(max_length=31)] = None
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserUpdate(schemas.BaseUserUpdate, UserPersonalDataUpdate):
    pass


class UserRead(schemas.BaseUser[UserIdType], UserProfileDataBase):
    groups: list[GroupBase] = []
    admin_groups: list[GroupBase] = []
    admin_tasks: list[TaskRead] = []

    class Config:
        from_attributes = True


class UserRegisteredNotification(BaseModel):
    user: UserRead
    ts: int
