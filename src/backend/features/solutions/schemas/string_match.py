from pydantic import BaseModel, ConfigDict

from features.solutions.schemas import BaseSolutionModel


class StringMatchSolutionModel(BaseSolutionModel):
    pass


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
