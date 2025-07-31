from features.modules.models import AccountModuleProgress, Module
from features.modules.schemas import ModuleReadWithProgress, ModuleReadWithTasks
from features.tasks.mappers import build_base_task_read_with_progress_list
from features.tasks.models import AccountTaskProgress, BaseTask


def build_module_read_with_progress(
    module: Module,
    account_module_progress: AccountModuleProgress | None = None,
) -> ModuleReadWithProgress:
    base_schema = module.get_validation_schema()

    return base_schema.to_with_progress(
        account_module_progress.user_completed_tasks_count
        if account_module_progress
        else 0
    )


def build_module_read_with_tasks(
    module: Module,
    account_module_progress: AccountModuleProgress,
    tasks: list[BaseTask],
    account_task_progresses: list[AccountTaskProgress],
) -> ModuleReadWithTasks:
    base_schema = module.get_validation_schema()
    tasks_schemas = build_base_task_read_with_progress_list(
        tasks, account_task_progresses
    )

    return base_schema.to_with_tasks(
        (
            account_module_progress.user_completed_tasks_count
            if account_module_progress
            else 0
        ),
        tasks_schemas,
    )


def build_module_read_with_progress_list(
    modules: list[Module],
    account_module_progresses: list[AccountModuleProgress],
) -> list[ModuleReadWithProgress]:
    account_progress_by_module_id: dict[int, AccountModuleProgress] = {}

    for progress in account_module_progresses:
        account_progress_by_module_id[progress.module_id] = progress

    return [
        build_module_read_with_progress(
            module, account_progress_by_module_id.get(module.id)
        )
        for module in modules
    ]
