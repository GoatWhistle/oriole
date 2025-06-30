from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from utils import get_number_one_bit_less as get_num_opt


class UserProfile(BaseModel):
    name: Annotated[str, Field(max_length=get_num_opt(30))]
    surname: Annotated[str, Field(max_length=get_num_opt(30))]
    patronymic: Annotated[Optional[str], Field(max_length=get_num_opt(30))] = None


class UserProfileRead(UserProfile):
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserAuth(BaseModel):
    email: Annotated[EmailStr, Field(max_length=get_num_opt(50))]
    hashed_password: Annotated[str, Field(max_length=get_num_opt(1000))]
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

    email: Annotated[EmailStr, Field(max_length=get_num_opt(50))]
    password: Annotated[str, Field(max_length=get_num_opt(1000))]
    name: Annotated[str, Field(max_length=get_num_opt(30))]
    surname: Annotated[str, Field(max_length=get_num_opt(30))]
    patronymic: Annotated[Optional[str], Field(max_length=get_num_opt(30))] = None


class RegisterUserInternal(RegisterUserInput):
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False


class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(max_length=get_num_opt(50))]
    password: Annotated[str, Field(max_length=get_num_opt(100))]


class UserRead(BaseModel):
    email: Annotated[EmailStr, Field(max_length=get_num_opt(50))]
    profile: UserProfileRead

    model_config = ConfigDict(
        from_attributes=True,
    )


class EmailChangeRequest(BaseModel):
    current_email: EmailStr
    new_email: EmailStr


class EmailUpdateRead(BaseModel):
    status: str
    message: str
    new_email: EmailStr


class UserProfileUpdate(BaseModel):
    name: Annotated[str, Field(max_length=get_num_opt(30))]
    surname: Annotated[str, Field(max_length=get_num_opt(30))]
    patronymic: Annotated[Optional[str], Field(max_length=get_num_opt(30))] = None


class UserProfileUpdatePartial(BaseModel):
    name: Annotated[str, Field(max_length=get_num_opt(30))] = None
    surname: Annotated[str, Field(max_length=get_num_opt(30))] = None
    patronymic: Annotated[Optional[str], Field(max_length=get_num_opt(30))] = None


class UserRole(BaseModel):
    user_role: int
    id: int
