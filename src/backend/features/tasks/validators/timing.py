from datetime import datetime

from features.tasks.exceptions import (
    TaskStartBeforeModuleStartException,
    TaskEndAfterModuleEndException,
)
from shared.validators import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
)


def check_task_start_deadline_after_module_start(
    task_start_deadline: datetime,
    module_start_deadline: datetime,
) -> None:
    if task_start_deadline < module_start_deadline:
        raise TaskStartBeforeModuleStartException()


def check_task_end_deadline_before_module_end(
    task_end_deadline: datetime,
    module_end_deadline: datetime,
) -> None:
    if task_end_deadline > module_end_deadline:
        raise TaskEndAfterModuleEndException()


def validate_task_deadlines(
    task_start: datetime,
    task_end: datetime,
    module_start: datetime,
    module_end: datetime,
) -> None:
    check_start_time_not_in_past(task_start)
    check_end_time_not_in_past(task_end)
    check_end_time_is_after_start_time(task_start, task_end)
    check_task_start_deadline_after_module_start(task_start, module_start)
    check_task_end_deadline_before_module_end(task_end, module_end)
