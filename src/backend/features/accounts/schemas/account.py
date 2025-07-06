from enum import IntEnum

from pydantic import BaseModel, Field, ConfigDict


class AccountRole(IntEnum):
    OWNER = 0
    ADMIN = 1
    MEMBER = 2


class AccountRead(BaseModel):
    id: int
    user_id: int
    space_id: int
    role: int

    model_config = ConfigDict(from_attributes=True)

    def to_with_profile_data(
        self,
        name: str,
        surname: str,
        patronymic: str,
    ) -> "AccountReadWithProfileData":
        return AccountReadWithProfileData(
            **self.model_dump(),
            name=name,
            surname=surname,
            patronymic=patronymic,
        )


class AccountReadWithProfileData(AccountRead):
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    patronymic: str = Field(max_length=30)
