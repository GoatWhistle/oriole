from datetime import datetime

from pydantic import BaseModel, ConfigDict

from features.solutions.schemas.solution_feedback import SolutionFeedbackRead


class BaseSolutionModel(BaseModel):
    task_id: int


class BaseSolutionCreate(BaseSolutionModel):
    pass


class BaseSolutionRead(BaseSolutionModel):
    id: int

    creator_id: int

    is_correct: bool = False
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def to_with_feedbacks(
        self, feedbacks: list[SolutionFeedbackRead]
    ) -> "BaseSolutionsReadWithFeedbacks":
        return BaseSolutionsReadWithFeedbacks(**self.model_dump(), feedbacks=feedbacks)


class BaseSolutionsReadWithFeedbacks(BaseSolutionRead):
    feedbacks: list[SolutionFeedbackRead]
