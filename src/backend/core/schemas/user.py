from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated, Optional


class UserProfile(BaseModel):
    name: Annotated[str, Field(max_length=31)]
    surname: Annotated[str, Field(max_length=31)]
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserProfileRead(UserProfile):
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


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


class RegisterUserInput(BaseModel):
    model_config = ConfigDict(strict=True)

    email: Annotated[EmailStr, Field(max_length=63)]
    password: Annotated[str, Field(max_length=1023)]
    name: Annotated[str, Field(max_length=31)]
    surname: Annotated[str, Field(max_length=31)]
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class RegisterUserInternal(RegisterUserInput):
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False


class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(max_length=63)]
    password: Annotated[str, Field(max_length=127)]


class UserRead(BaseModel):
    email: Annotated[EmailStr, Field(max_length=63)]
    profile: UserProfileRead

    model_config = ConfigDict(
        from_attributes=True,
    )


class EmailUpdate(BaseModel):
    email: Annotated[Optional[EmailStr], Field(max_length=63)]


class EmailUpdateRead(EmailUpdate):
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserProfileUpdate(BaseModel):
    name: Annotated[str, Field(max_length=31)]
    surname: Annotated[str, Field(max_length=31)]
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None


class UserProfileUpdatePartial(BaseModel):
    name: Annotated[str, Field(max_length=31)] = None
    surname: Annotated[str, Field(max_length=31)] = None
    patronymic: Annotated[Optional[str], Field(max_length=63)] = None
