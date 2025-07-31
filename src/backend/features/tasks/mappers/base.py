import features.solutions.mappers as solution_mapper
from features.solutions.models import BaseSolution
from features.tasks.models import AccountTaskProgress, BaseTask
from features.tasks.schemas import (
    BaseTaskReadWithProgress,
    BaseTaskReadWithSolutions,
)


def build_base_task_read_with_progress(
    task: BaseTask,
    account_task_progress: AccountTaskProgress | None = None,
) -> BaseTaskReadWithProgress:
    base_schema = task.get_validation_schema()
    return base_schema.to_with_progress(
        account_task_progress.is_correct if account_task_progress else False,
        account_task_progress.user_attempts if account_task_progress else 0,
    )


def build_base_task_read_with_solutions(
    task: BaseTask,
    solutions: list[BaseSolution],
    account_task_progress: AccountTaskProgress | None = None,
) -> BaseTaskReadWithSolutions:
    base_schema = task.get_validation_schema()
    solutions_read = solution_mapper.build_base_solution_read_list(solutions)
    return base_schema.to_with_solutions(
        account_task_progress.is_correct if account_task_progress else False,
        account_task_progress.user_attempts if account_task_progress else 0,
        solutions_read,
    )


def build_base_task_read_with_progress_list(
    tasks: list[BaseTask],
    account_task_progresses: list[AccountTaskProgress],
) -> list[BaseTaskReadWithProgress]:
    account_progress_by_task_id: dict[int, AccountTaskProgress] = {}

    for progress in account_task_progresses:
        account_progress_by_task_id[progress.task_id] = progress

    return [
        build_base_task_read_with_progress(
            task, account_progress_by_task_id.get(task.id)
        )
        for task in tasks
    ]
