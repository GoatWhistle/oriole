from features.modules.models import Module
from features.modules.schemas import ModuleRead, ModuleReadWithPerformance
from features.solutions.models import BaseSolution
from features.tasks.mappers import build_base_task_read_with_correctness_list
from features.tasks.models import BaseTask


def build_module_read_with_performance(
    module: Module,
    tasks: list[BaseTask],
    solutions: list[BaseSolution],
) -> ModuleReadWithPerformance:
    tasks_schemas = build_base_task_read_with_correctness_list(tasks, solutions)
    user_completed_tasks_count = sum(1 for task in tasks_schemas if task.is_correct)
    base_schema = module.get_validation_schema()

    return base_schema.to_with_performance(user_completed_tasks_count)


def build_module_read_with_tasks(
    module: Module,
    tasks: list[BaseTask],
    solutions: list[BaseSolution],
) -> ModuleReadWithPerformance:
    tasks_schemas = build_base_task_read_with_correctness_list(tasks, solutions)
    user_completed_tasks_count = sum(1 for task in tasks_schemas if task.is_correct)
    base_schema = module.get_validation_schema()

    return base_schema.to_with_tasks(user_completed_tasks_count, tasks_schemas)


def build_module_read_with_performance_list(
    modules: list[Module],
    tasks: list[BaseTask],
    solutions: list[BaseSolution] | None,
) -> list[ModuleRead]:
    return [
        build_module_read_with_performance(module, tasks, solutions)
        for module in modules
    ]
