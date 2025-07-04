from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class BaseSolutionModel(BaseModel):
    submitted_at: datetime


class BaseSolutionCreate(BaseSolutionModel):
    task_id: int


class BaseSolutionRead(BaseSolutionModel):
    id: int
    account_id: int
    task_id: int
    module_id: int
    space_id: int
    is_correct: bool
    user_attempts: int

    model_config = ConfigDict(from_attributes=True)
