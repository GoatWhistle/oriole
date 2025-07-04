from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSolutionModel(BaseModel):
    task_id: int


class BaseSolutionCreate(BaseSolutionModel):
    pass


class BaseSolutionRead(BaseSolutionModel):
    id: int

    account_id: int

    is_correct: bool = False
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)
