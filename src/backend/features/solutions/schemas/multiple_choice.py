from features.solutions.schemas.base import (
    BaseSolutionModel,
    BaseSolutionCreate,
    BaseSolutionRead,
    BaseSolutionsReadWithFeedbacks,
)
from features.solutions.schemas.solution_feedback import SolutionFeedbackRead


class MultipleChoiceSolutionBase(BaseSolutionModel):
    pass


class MultipleChoiceSolutionCreate(MultipleChoiceSolutionBase, BaseSolutionCreate):
    user_answer: list


class MultipleChoiceSolutionRead(MultipleChoiceSolutionBase, BaseSolutionRead):
    def to_with_feedbacks(
        self, feedbacks: list[SolutionFeedbackRead]
    ) -> "MultipleChoiceReadWithFeedbacks":
        return MultipleChoiceReadWithFeedbacks(**self.model_dump(), feedbacks=feedbacks)


class MultipleChoiceReadWithFeedbacks(
    MultipleChoiceSolutionRead, BaseSolutionsReadWithFeedbacks
):
    pass
