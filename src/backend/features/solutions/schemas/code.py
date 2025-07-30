from features.solutions.schemas.base import (
    BaseSolutionModel,
    BaseSolutionCreate,
    BaseSolutionRead,
    BaseSolutionsReadWithFeedbacks,
)

from features.solutions.schemas.solution_feedback import SolutionFeedbackRead


class CodeSolutionBase(BaseSolutionModel):
    code: str


class CodeSolutionCreate(CodeSolutionBase, BaseSolutionCreate):
    pass


class CodeSolutionRead(CodeSolutionBase, BaseSolutionRead):
    status: str

    def to_with_feedbacks(
        self, feedbacks: list[SolutionFeedbackRead]
    ) -> "CodeSolutionReadWithFeedbacks":
        return CodeSolutionReadWithFeedbacks(**self.model_dump(), feedbacks=feedbacks)


class CodeSolutionReadWithFeedbacks(CodeSolutionRead, BaseSolutionsReadWithFeedbacks):
    pass
