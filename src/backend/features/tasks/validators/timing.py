from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Mapped

from features.modules.models import Module
from features.tasks.models import Task
from utils import get_current_utc


async def check_deadline_not_passed(
    task: Task,
) -> None:
    if not task.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deadline for task {task.id} has already passed",
        )


async def check_start_time_not_in_past(
    task: Task,
    start_datetime: datetime | Mapped[datetime],
) -> None:
    if start_datetime < get_current_utc():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Start time of task {task.id} cannot be in the past.",
        )


async def check_end_time_not_in_past(
    task: Task,
    end_datetime: datetime | Mapped[datetime],
) -> None:
    if end_datetime < get_current_utc():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"End time of task {task.id} cannot be in the past.",
        )


async def check_end_time_is_after_start_time(
    task: Task,
    start_datetime: datetime | Mapped[datetime],
    end_datetime: datetime | Mapped[datetime],
) -> None:
    if start_datetime >= end_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"End time of task {task.id} must be after start time.",
        )


async def check_task_start_deadline_before_module_start(
    task: Task,
    module: Module,
    task_start_deadline: datetime | Mapped[datetime],
    module_start_deadline: datetime | Mapped[datetime],
) -> None:
    if task_start_deadline < module_start_deadline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task {task.id} start deadline cannot be earlier than module {module.id} start deadline.",
        )


async def check_task_end_deadline_after_module_end(
    task: Task,
    module: Module,
    task_end_deadline: datetime | Mapped[datetime],
    module_end_deadline: datetime | Mapped[datetime],
) -> None:
    if task_end_deadline > module_end_deadline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task {task.id} end deadline cannot be later than module {module.id} end deadline.",
        )
