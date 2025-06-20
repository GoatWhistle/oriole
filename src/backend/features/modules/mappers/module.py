from typing import Sequence

from features.modules.models import Module
from features.modules.schemas import ModuleRead
from features.modules.schemas import ModuleReadPartial
from features.tasks.models import Task, UserReply
from features.tasks.schemas import TaskReadPartial


def build_module_read(
    module: Module,
    group_id: int,
    tasks: Sequence[Task] | None = None,
    user_replies_by_task_id: dict[int, UserReply] | None = None,
) -> ModuleRead:
    tasks = tasks or []
    user_replies_by_task_id = user_replies_by_task_id or {}
    user_completed_tasks_count = sum(
        1 for reply in user_replies_by_task_id.values() if reply.is_correct
    )
    return ModuleRead(
        id=module.id,
        group_id=group_id,
        title=module.title,
        description=module.description,
        is_contest=module.is_contest,
        tasks_count=len(tasks),
        user_completed_tasks_count=user_completed_tasks_count,
        is_active=module.is_active,
        admin_id=module.admin_id,
        start_datetime=module.start_datetime,
        end_datetime=module.end_datetime,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=(
                    user_replies_by_task_id.get(task.id).is_correct
                    if user_replies_by_task_id and task.id in user_replies_by_task_id
                    else False
                ),
                is_active=task.is_active,
            )
            for task in tasks
        ],
    )


def build_module_read_partial(
    module: Module,
    tasks_count: int,
    user_replies: Sequence[UserReply],
) -> ModuleReadPartial:
    replies_by_task_id = {reply.task_id: reply for reply in user_replies}
    user_completed_tasks_count = sum(
        1 for reply in replies_by_task_id.values() if reply.is_correct
    )

    return ModuleReadPartial(
        id=module.id,
        title=module.title,
        description=module.description,
        is_contest=module.is_contest,
        tasks_count=tasks_count,
        user_completed_tasks_count=user_completed_tasks_count,
        is_active=module.is_active,
    )


def build_module_read_partial_list(
    modules_with_counts: Sequence[tuple[Module, int]],
    tasks_by_module_id: dict[int, list[Task]],
    user_replies_by_task_id: dict[int, UserReply],
) -> Sequence[ModuleReadPartial]:
    module_read_list = []

    for module, tasks_count in modules_with_counts:
        module_tasks = tasks_by_module_id.get(module.id, [])

        completed_count = sum(
            1
            for task in module_tasks
            if (reply := user_replies_by_task_id.get(task.id)) and reply.is_correct
        )

        module_read_list.append(
            ModuleReadPartial(
                id=module.id,
                title=module.title,
                description=module.description,
                is_contest=module.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=completed_count,
                is_active=module.is_active,
            )
        )

    return module_read_list
