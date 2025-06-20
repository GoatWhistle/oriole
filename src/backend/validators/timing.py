from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Mapped

from utils import get_current_utc


def _get_obj_info(
    obj: Any = None, *, obj_name: str = None, obj_id: int = None
) -> tuple[str, int | None]:
    if obj is not None:
        obj_name = obj.__class__.__name__.lower()
        obj_id = getattr(obj, "id", None)
    elif obj_name is None:
        raise ValueError("Either 'obj' or 'obj_name' must be provided")
    return obj_name, obj_id


def check_deadline_not_passed(obj) -> None:
    if not obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deadline for {obj.__name__.lower()} {obj.id} has already passed",
        )


def check_start_time_not_in_past(
    start_datetime: datetime | Mapped[datetime],
    *,
    obj: Any = None,
    obj_name: str = None,
    obj_id: int = None,
) -> None:
    obj_name, obj_id = _get_obj_info(obj, obj_name=obj_name, obj_id=obj_id)
    if start_datetime < get_current_utc():
        detail = f"Start time of {obj_name}"
        if obj_id is not None:
            detail += f" {obj_id}"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail + " cannot be in the past.",
        )


def check_end_time_not_in_past(
    end_datetime: datetime | Mapped[datetime],
    *,
    obj: Any = None,
    obj_name: str = None,
    obj_id: int = None,
) -> None:
    obj_name, obj_id = _get_obj_info(obj, obj_name=obj_name, obj_id=obj_id)
    if end_datetime < get_current_utc():
        detail = f"End time of {obj_name}"
        if obj_id is not None:
            detail += f" {obj_id}"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail + "cannot be in the past.",
        )


def check_end_time_is_after_start_time(
    start_datetime: datetime | Mapped[datetime],
    end_datetime: datetime | Mapped[datetime],
    *,
    obj: Any = None,
    obj_name: str = None,
    obj_id: int = None,
) -> None:
    obj_name, obj_id = _get_obj_info(obj, obj_name=obj_name, obj_id=obj_id)
    if start_datetime >= end_datetime:
        detail = f"End time of {obj_name}"
        if obj_id is not None:
            detail += f" {obj_id}"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail + " must be after start time.",
        )
