import features.solutions.mappers as solution_mapper
from features.solutions.models import BaseSolution
from features.tasks.models import BaseTask
from features.tasks.schemas import (
    BaseTaskReadWithCorrectness,
    BaseTaskRead,
    BaseTaskReadWithSolutions,
)


def build_base_task_read_with_correctness(
    task: BaseTask,
    solutions: list[BaseSolution] | None = None,
) -> BaseTaskReadWithCorrectness:
    task_read: BaseTaskRead = task.get_validation_schema()
    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions) if solutions else 0

    return BaseTaskReadWithCorrectness(
        **task_read.model_dump(),
        is_correct=is_correct,
        user_attempts=user_attempts,
    )


def build_base_task_read_with_solutions(
    task: BaseTask,
    solutions: list[BaseSolution],
) -> BaseTaskReadWithSolutions:
    task_read: BaseTaskRead = task.get_validation_schema()
    is_correct = any(sol.is_correct for sol in solutions)
    user_attempts = len(solutions)
    solutions_read = solution_mapper.build_base_solution_read_list(solutions)

    return BaseTaskReadWithSolutions(
        **task_read.model_dump(),
        is_correct=is_correct,
        user_attempts=user_attempts,
        solutions=solutions_read,
    )


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
