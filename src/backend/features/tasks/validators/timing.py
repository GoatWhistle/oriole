from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Mapped

from features.modules.models import Module
from features.tasks.models import Task


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
