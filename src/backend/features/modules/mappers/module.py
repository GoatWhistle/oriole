import features.tasks.mappers as mapper
from features import StringMatchSolution
from features.modules.models import Module
from features.modules.schemas import ModuleRead
from features.modules.schemas.module import (
    ModuleReadWithoutReplies,
    ModuleReadWithoutTasks,
)
from features.tasks.models import StringMatchTask


def build_module_read(
    module: Module,
    tasks: list[StringMatchTask] | None = None,
    solutions: list[StringMatchSolution] | None = None,
) -> ModuleRead | ModuleReadWithoutReplies | ModuleReadWithoutTasks:
    tasks = tasks or []
    solutions = solutions or []

    task_reads = mapper.build_task_read_list([module], tasks, solutions)
    user_completed_tasks_count = (
        sum(task.is_correct for task in task_reads) if solutions else None
    )

    base_data = {
        "id": module.id,
        "title": module.title,
        "description": module.description,
        "start_datetime": module.start_datetime,
        "end_datetime": module.end_datetime,
        "is_active": module.is_active,
        "space_id": module.space_id,
        "creator_id": module.creator_id,
        "tasks_count": module.tasks_count,
    }
    model_class: type[ModuleRead | ModuleReadWithoutReplies | ModuleReadWithoutTasks]

    match (bool(tasks), bool(solutions)):
        case (True, True):
            model_class = ModuleRead
            extra_data = {
                "tasks": task_reads,
                "user_completed_tasks_count": user_completed_tasks_count,
            }
        case (True, False):
            model_class = ModuleReadWithoutReplies
            extra_data = {"tasks": task_reads}
        case _:
            model_class = ModuleReadWithoutTasks
            extra_data = {}

    return model_class(**base_data, **extra_data)


def build_module_read_list(
    modules: list[Module],
    tasks: list[StringMatchTask] | None,
    solutions: list[StringMatchSolution] | None,
) -> list[ModuleRead]:
    return [
        build_module_read(
            module=module,
            tasks=tasks,
            solutions=solutions,
        )
        for module in modules
    ]
