from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Mapped

from features.modules.models import Module
from features.tasks.models import Task
from utils import get_current_utc


async def check_deadline_not_passed(
    obj: Module | Task,
) -> None:
    if not obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deadline for {obj.__name__.lower()} {obj.id} has already passed",
        )


async def check_start_time_not_in_past(
    obj: Module | Task,
    start_datetime: datetime | Mapped[datetime],
) -> None:
    if start_datetime < get_current_utc():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Start time of {obj.__name__.lower()} {obj.id} cannot be in the past.",
        )


async def check_end_time_not_in_past(
    obj: Module | Task,
    end_datetime: datetime | Mapped[datetime],
) -> None:
    if end_datetime < get_current_utc():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"End time of {obj.__name__.lower()} {obj.id} cannot be in the past.",
        )


async def check_end_time_is_after_start_time(
    obj: Module | Task,
    start_datetime: datetime | Mapped[datetime],
    end_datetime: datetime | Mapped[datetime],
) -> None:
    if start_datetime >= end_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"End time of {obj.__name__.lower()} {obj.id} must be after start time.",
        )
