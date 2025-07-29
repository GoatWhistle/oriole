from features.solutions.schemas import BaseSolutionModel


class BaseFeedbackModel(BaseSolutionModel):
    feedback: str
    solution_id: int


class MultipleChoiceFeedback(BaseFeedbackModel):
    pass


class StringMathcFeedback(BaseFeedbackModel):
    pass
