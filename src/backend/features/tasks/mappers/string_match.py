from features.tasks.models import AccountTaskProgress, StringMatchTask
from features.tasks.schemas import StringMatchTaskReadWithProgress


def build_string_match_task_read_with_correctness(
    task: StringMatchTask,
    account_task_progress: AccountTaskProgress | None = None,
) -> StringMatchTaskReadWithProgress:
    base_schema = task.get_validation_schema()
    return base_schema.to_with_progress(
        account_task_progress.is_correct if account_task_progress else False,
        account_task_progress.user_attempts_count if account_task_progress else 0,
    )
