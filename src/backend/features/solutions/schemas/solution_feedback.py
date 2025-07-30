from datetime import datetime

from pydantic import BaseModel, model_validator, ConfigDict


class SolutionFeedbackBase(BaseModel):
    content: str
    is_anonymous: bool = False


class SolutionFeedbackCreate(SolutionFeedbackBase):
    pass


class SolutionFeedbackRead(SolutionFeedbackBase):
    id: int
    solution_id: int
    creator_id: int | None = None
    updated_at: datetime
    is_updated: bool

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def hide_account_if_anonymous(self):
        if self.is_anonymous:
            self.creator_id = None
        return self


class SolutionFeedbackUpdate(SolutionFeedbackBase):
    content: str | None = None
    is_anonymous: bool | None = None
