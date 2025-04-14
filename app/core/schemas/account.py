from typing import Sequence

from pydantic import BaseModel, ConfigDict

from enum import IntEnum


class AccountRole(IntEnum):
    TEACHER = 0
    STUDENT = 1


class Account(BaseModel):
    user_id: int

    role: AccountRole

    group_id: int

    done_tasks: Sequence[int]
