from features.solutions.models import SolutionFeedback
from features.solutions.schemas import SolutionFeedbackRead


def build_base_solution_feedback_read_list(
    solution_feedbacks: list[SolutionFeedback],
) -> list[SolutionFeedbackRead]:
    return [
        solution_feedback.get_validation_schema()
        for solution_feedback in solution_feedbacks
    ]
