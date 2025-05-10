from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserReplyBase(BaseModel):
    account_id: int
    task_id: int
    user_answer: str
    is_correct: bool
    user_attempts: int


class UserReplyRead(UserReplyBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserReplyCreate(UserReplyBase):
    pass


class UserReplyUpdate(UserReplyBase):
    user_answer: Optional[str] = None
    is_correct: Optional[bool] = None
