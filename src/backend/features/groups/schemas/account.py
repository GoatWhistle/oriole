from enum import IntEnum

from pydantic import BaseModel

from features.users.schemas import UserProfileRead


class AccountRole(IntEnum):
    OWNER = 0
    ADMIN = 1
    MEMBER = 2


class AccountRead(BaseModel):
    user_profile: UserProfileRead
    role: int


class AccountRoleChangeRead(BaseModel):
    group_id: int
    user_id: int
