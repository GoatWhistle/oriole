from typing import Sequence

from pydantic import BaseModel

from enum import IntEnum


from core.schemas.task import TaskRead


class AccountRole(IntEnum):
    OWNER = 0
    ADMIN = 1
    MEMBER = 2


class AccountRead(BaseModel):
    user_id: int

    role: int

    group_id: int

    done_tasks: Sequence[TaskRead]
