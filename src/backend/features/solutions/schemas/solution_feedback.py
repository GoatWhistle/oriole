from datetime import datetime

from pydantic import BaseModel, model_validator


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

    @model_validator(mode="before")
    def hide_account_if_anonymous(cls, data: dict) -> dict:
        if data.get("is_anonymous"):
            data["creator_id"] = None
        return data


class SolutionFeedbackUpdate(SolutionFeedbackBase):
    content: str | None = None
    is_anonymous: bool | None = None
