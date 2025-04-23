from typing import Sequence
from pydantic import BaseModel
from enum import IntEnum
from core.schemas.user_reply import UserReplyRead


class AccountRole(IntEnum):
    OWNER = 0
    ADMIN = 1
    MEMBER = 2


class AccountRead(BaseModel):
    user_id: int
    group_id: int

    role: int
    done_tasks: Sequence[UserReplyRead]
