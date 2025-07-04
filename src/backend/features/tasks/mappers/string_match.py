from features.solutions.models import StringMatchSolution
from features.tasks.models import StringMatchTask
from features.tasks.schemas import StringMatchTaskReadWithCorrectness


def build_string_match_task_read_with_correctness(
    task: StringMatchTask,
    solutions: list[StringMatchSolution],
) -> StringMatchTaskReadWithCorrectness:
    task_read = task.get_validation_schema()
    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions) if solutions else 0
    return StringMatchTaskReadWithCorrectness(
        **task_read.model_dump(),
        is_correct=is_correct,
        user_attempts=user_attempts,
    )
