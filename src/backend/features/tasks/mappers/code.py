from features.solutions.models import CodeSolution
from features.tasks.models import CodeTask
from features.tasks.schemas import CodeTaskReadWithCorrectness


def build_code_task_read_with_correctness(
    task: CodeTask,
    solutions: list[CodeSolution],
) -> CodeTaskReadWithCorrectness:
    task_read = task.get_validation_schema()
    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions) if solutions else 0
    return CodeTaskReadWithCorrectness(
        **task_read.model_dump(),
        is_correct=is_correct,
        user_attempts=user_attempts,
    )
