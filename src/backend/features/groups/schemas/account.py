from enum import IntEnum

from pydantic import BaseModel


class AccountRole(IntEnum):
    OWNER = 0
    ADMIN = 1
    MEMBER = 2


class AccountReadPartial(BaseModel):
    user_id: int
    role: int
