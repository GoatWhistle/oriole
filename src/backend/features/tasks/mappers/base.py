import features.solutions.mappers as solution_mapper
from features.solutions.models import BaseSolution
from features.tasks.models import BaseTask
from features.tasks.schemas import (
    BaseTaskReadWithCorrectness,
    BaseTaskReadWithSolutions,
)


def build_base_task_read_with_correctness(
    task: BaseTask,
    solutions: list[BaseSolution] | None = None,
) -> BaseTaskReadWithCorrectness:
    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions) if solutions else 0
    base_schema = task.get_validation_schema()

    return base_schema.to_with_correctness(is_correct, user_attempts)


def build_base_task_read_with_solutions(
    task: BaseTask,
    solutions: list[BaseSolution],
) -> BaseTaskReadWithSolutions:
    is_correct = any(sol.is_correct for sol in solutions)
    user_attempts = len(solutions)
    base_schema = task.get_validation_schema()
    solutions_read = solution_mapper.build_base_solution_read_list(solutions)

    return base_schema.to_with_solutions(is_correct, user_attempts, solutions_read)


def build_base_task_read_with_correctness_list(
    tasks: list[BaseTask],
    solutions: list[BaseSolution],
) -> list[BaseTaskReadWithCorrectness]:
    solutions_by_task_id: dict[int, list[BaseSolution]] = {}

    for solution in solutions:
        solutions_by_task_id.setdefault(solution.task_id, []).append(solution)

    return [
        build_base_task_read_with_correctness(
            task, solutions_by_task_id.get(task.id, [])
        )
        for task in tasks
    ]
