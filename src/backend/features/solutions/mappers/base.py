import features.solutions.mappers as solution_mapper
from features.solutions.models import BaseSolution, SolutionFeedback
from features.solutions.schemas import BaseSolutionRead, BaseSolutionsReadWithFeedbacks


def build_base_solution_read_with_feedbacks(
    solution: BaseSolution,
    feedbacks: list[SolutionFeedback],
) -> BaseSolutionsReadWithFeedbacks:
    base_schema = solution.get_validation_schema()
    feedbacks_read = solution_mapper.build_base_solution_feedback_read_list(feedbacks)

    return base_schema.to_with_feedbacks(feedbacks_read)


def build_base_solution_read_list(
    solutions: list[BaseSolution],
) -> list[BaseSolutionRead]:
    return [solution.get_validation_schema() for solution in solutions]
