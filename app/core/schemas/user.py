from pydantic import BaseModel, EmailStr, Field, constr, ConfigDict
from typing import Annotated, Optional, Union
from fastapi_users import schemas

from core.types.user_id import UserIdType


class UserProfile(BaseModel):
    user_id: int
    name: Annotated[str, Field(max_length=31)]
    surname: Annotated[str, Field(max_length=31)]
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserAuth(BaseModel):
    email: Annotated[EmailStr, Field(max_length=63)]
    hashed_password: Annotated[str, Field(max_length=1023)]
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False


class UserAuthRead(UserAuth):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class RegisterUser(BaseModel):
    email: Annotated[EmailStr, Field(max_length=63)]
    hashed_password: Annotated[str, Field(max_length=1023)]
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False
    name: Annotated[str, Field(max_length=31)]
    surname: Annotated[str, Field(max_length=31)]
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserCreate(BaseModel):
    pass


class UserProfileUpdatePartial(BaseModel):
    name: Annotated[Optional[str], Field(max_length=31)] = None
    surname: Annotated[Optional[str], Field(max_length=31)] = None
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserUpdate(UserProfileUpdatePartial):
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
