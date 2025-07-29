from features.solutions.models import MultipleChoiceSolution
from features.tasks.models import MultipleChoiceTask
from features.tasks.schemas import MultipleChoiceTaskReadWithCorrectness


def build_multiple_choice_task_read_with_correctness(
    task: MultipleChoiceTask,
    solutions: list[MultipleChoiceSolution],
) -> MultipleChoiceTaskReadWithCorrectness:
    task_read = task.get_validation_schema()
    is_correct = any(sol.is_correct for sol in solutions) if solutions else False
    user_attempts = len(solutions) if solutions else 0
    return MultipleChoiceTaskReadWithCorrectness(
        **task_read.model_dump(),
        is_correct=is_correct,
        user_attempts=user_attempts,
    )
