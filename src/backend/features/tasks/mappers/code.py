from features.tasks.models import AccountTaskProgress, CodeTask
from features.tasks.schemas import CodeTaskReadWithProgress


def build_code_task_read_with_progress(
    task: CodeTask,
    account_task_progress: AccountTaskProgress | None = None,
) -> CodeTaskReadWithProgress:
    base_schema = task.get_validation_schema()
    return base_schema.to_with_progress(
        account_task_progress.is_correct if account_task_progress else False,
        account_task_progress.user_attempts_count if account_task_progress else 0,
    )
