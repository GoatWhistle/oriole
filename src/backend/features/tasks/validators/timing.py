from datetime import datetime

from features.tasks.exceptions import (
    TaskStartBeforeModuleStartException,
    TaskEndAfterModuleEndException,
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
