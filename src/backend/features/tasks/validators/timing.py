from datetime import datetime

from fastapi import HTTPException, status


def check_task_start_deadline_after_module_start(
    task_start_deadline: datetime,
    module_start_deadline: datetime,
    task_id: int | None = None,
    module_id: int | None = None,
) -> None:
    if task_start_deadline < module_start_deadline:
        detail = "Task start deadline cannot be earlier than module start deadline."
        if task_id is not None and module_id is not None:
            detail = f"Task {task_id} start deadline cannot be earlier than module {module_id} start deadline."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


def check_task_end_deadline_before_module_end(
    task_end_deadline: datetime,
    module_end_deadline: datetime,
    task_id: int | None = None,
    module_id: int | None = None,
) -> None:
    if task_end_deadline > module_end_deadline:
        detail = "Task end deadline cannot be later than module end deadline."
        if task_id is not None and module_id is not None:
            detail = f"Task {task_id} end deadline cannot be later than module {module_id} end deadline."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
