from typing import Sequence

from features.solutions.models import BaseSolution
from features.solutions.schemas.base import BaseSolutionRead


def build_base_solution_read_list(
    solutions: Sequence[BaseSolution],
) -> list[BaseSolutionRead]:
    return [solution.get_validation_schema() for solution in solutions]
