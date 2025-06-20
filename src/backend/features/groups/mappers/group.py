from collections.abc import Sequence

from features.groups.models import Group, Account
from features.groups.schemas import GroupRead, AccountReadPartial
from features.modules.models import Module
from features.modules.schemas import ModuleReadPartial
from features.tasks.models import Task, UserReply


def build_group_read(
    group: Group,
    accounts: Sequence[Account],
    modules: Sequence[tuple[Module, int]] | None = None,
    task_map: dict[int, Sequence[Task]] | None = None,
    user_replies_by_task_id: dict[int, UserReply] | None = None,
) -> GroupRead:
    task_map = task_map or {}
    user_replies_by_task_id = user_replies_by_task_id or {}
    modules = modules or []

    group_modules = []
    for module, tasks_count in modules:
        module_tasks = task_map.get(module.id, [])

        completed_count = (
            sum(
                1
                for task in module_tasks
                if (reply := user_replies_by_task_id.get(task.id)) and reply.is_correct
            )
            if user_replies_by_task_id
            else 0
        )

        group_modules.append(
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

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=[
            AccountReadPartial.model_validate(account.__dict__) for account in accounts
        ],
        modules=group_modules,
    )
