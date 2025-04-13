from pydantic import BaseModel, EmailStr, Field, constr, ConfigDict
from typing import Annotated, Optional, TYPE_CHECKING
from fastapi_users import schemas

from core.types.user_id import UserIdType


class UserProfile(BaseModel):
    name: Annotated[constr(max_length=31), Field(example="Иван")]
    surname: Annotated[constr(max_length=31), Field(example="Петров")]
    patronymic: Annotated[
        Optional[constr(max_length=63)], Field(example="Сергеевич")
    ] = None
    email: Annotated[EmailStr, Field(example="user@example.com")]


class UserCreate(schemas.BaseUserCreate, UserProfile):
    pass


class UserProfileUpdatePartial(BaseModel):
    name: Annotated[Optional[str], Field(max_length=31)] = None
    surname: Annotated[Optional[str], Field(max_length=31)] = None
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserUpdate(schemas.BaseUserUpdate, UserProfileUpdatePartial):
    pass


class UserRead(schemas.BaseUser[UserIdType], UserProfile):
    id: int

    accounts: list[Optional[int]]
    done_tasks: list[Optional[int]]

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserRegisteredNotification(BaseModel):
    user_id: int
    ts: int
