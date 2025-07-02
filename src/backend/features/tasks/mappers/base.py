from collections import defaultdict

from features.solutions.models import BaseSolution
from features.tasks.models import BaseTask
from features.tasks.schemas import BaseTaskRead


def build_base_task_reads_list(
    tasks: list[BaseTask],
    solutions: list[BaseSolution],
) -> list[BaseTaskRead]:
    solutions_grouped: dict[int, list[BaseSolution]] = defaultdict(list)
    for solution in solutions:
        solutions_grouped[solution.task_id].append(solution)

    result = []
    for task in tasks:
        solutions = solutions_grouped.get(task.id, [])

        task_read = task.get_validation_schema(
            is_correct=any(sol.is_correct for sol in solutions),
            user_attempts=len(solutions),
        )

        result.append(task_read)

    return result
