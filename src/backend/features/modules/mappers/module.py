import features.tasks.mappers as mapper
from features.modules.models import Module
from features.modules.schemas import ModuleRead
from features.tasks.models import Task, UserReply


def build_module_read(
    module: Module,
    tasks: list[Task] | None = None,
    user_replies: list[UserReply] | None = None,
) -> ModuleRead:
    tasks = tasks or []
    user_replies = user_replies or []

    task_reads = mapper.build_task_read_list([module], tasks, user_replies)
    user_completed_tasks_count = sum(task.is_correct for task in task_reads)

    return ModuleRead(
        title=module.title,
        description=module.description,
        start_datetime=module.start_datetime,
        end_datetime=module.end_datetime,
        is_contest=module.is_contest,
        id=module.id,
        is_active=module.is_active,
        group_id=module.group_id,
        admin_id=module.admin_id,
        tasks_count=len(tasks),
        user_completed_tasks_count=user_completed_tasks_count,
        tasks=task_reads,
    )


def build_module_read_list(
    modules: list[Module],
    tasks: list[Task],
    user_replies: list[UserReply],
) -> list[ModuleRead]:
    return [
        build_module_read(
            module=module,
            tasks=tasks,
            user_replies=user_replies,
        )
        for module in modules
    ]
