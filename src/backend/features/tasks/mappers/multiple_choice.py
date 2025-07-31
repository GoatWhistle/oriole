from features.tasks.models import AccountTaskProgress, MultipleChoiceTask
from features.tasks.schemas import MultipleChoiceTaskReadWithProgress


def build_multiple_choice_task_read_with_progress(
    task: MultipleChoiceTask,
    account_task_progress: AccountTaskProgress | None = None,
) -> MultipleChoiceTaskReadWithProgress:
    base_schema = task.get_validation_schema()
    return base_schema.to_with_progress(
        account_task_progress.is_correct if account_task_progress else False,
        account_task_progress.user_attempts if account_task_progress else 0,
    )
