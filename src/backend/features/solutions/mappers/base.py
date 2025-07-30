from features.solutions.models import BaseSolution
from features.solutions.schemas import BaseSolutionRead


def build_base_solution_read_list(
    solutions: list[BaseSolution],
) -> list[BaseSolutionRead]:
    return [solution.get_validation_schema() for solution in solutions]
