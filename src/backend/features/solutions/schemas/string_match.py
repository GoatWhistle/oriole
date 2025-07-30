from pydantic import Field

from features.solutions.schemas.base import (
    BaseSolutionModel,
    BaseSolutionCreate,
    BaseSolutionRead,
    BaseSolutionsReadWithFeedbacks,
)
from features.solutions.schemas.solution_feedback import SolutionFeedbackRead


class StringMatchSolutionBase(BaseSolutionModel):
    pass


class StringMatchSolutionCreate(StringMatchSolutionBase, BaseSolutionCreate):
    user_answer: str = Field(max_length=300)


class StringMatchSolutionRead(StringMatchSolutionBase, BaseSolutionRead):
    def to_with_feedbacks(
        self, feedbacks: list[SolutionFeedbackRead]
    ) -> "StringMatchSolutionReadWithFeedbacks":
        return StringMatchSolutionReadWithFeedbacks(
            **self.model_dump(), feedbacks=feedbacks
        )


class StringMatchSolutionReadWithFeedbacks(
    StringMatchSolutionRead, BaseSolutionsReadWithFeedbacks
):
    pass
