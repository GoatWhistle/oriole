from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.models import Task, UserReply
from utils.time_manager import get_current_utc_timestamp


async def get_task_if_exists(
    session: AsyncSession,
    task_id: Mapped[int] | int,
) -> Task:
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task


async def check_counter_limit(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    user_reply_id: Mapped[int] | int,
    task: Task,
) -> None:
    user_reply = await session.get(UserReply, user_reply_id)
    if user_reply.user_attempts >= task.max_attempts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The number of user {user_id} attempts is more than the number of maximum attempts of task {task.id}",
        )


async def check_task_is_already_correct(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    user_reply_id: Mapped[int] | int,
    task: Task,
) -> None:
    user_reply = await session.get(UserReply, user_reply_id)

    if user_reply and user_reply.is_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Task {task.id} has already been solved correctly by user {user_id}.",
        )


async def check_deadline_not_passed(
    task: Task,
) -> None:
    if not task.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deadline for task {task} has already passed",
        )


async def check_end_time_is_after_start_time(
    start_datetime: int | Mapped[int],
    end_datetime: int | Mapped[int],
) -> None:
    if start_datetime >= end_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )


async def check_start_time_not_in_past(
    start_datetime: int | Mapped[int],
) -> None:
    if start_datetime < get_current_utc_timestamp():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time cannot be in the past.",
        )


async def check_end_time_not_in_past(
    end_datetime: int | Mapped[int],
) -> None:
    if end_datetime < get_current_utc_timestamp() :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time cannot be in the past.",
        )


async def check_task_start_deadline_before_assignment_start(
    task_start_deadline: int | Mapped[int],
    assignment_start_deadline: int | Mapped[int],
) -> None:
    if task_start_deadline < assignment_start_deadline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task start deadline cannot be earlier than assignment start deadline.",
        )


async def check_task_end_deadline_after_assignment_end(
    task_end_deadline: int | Mapped[int],
    assignment_end_deadline: int | Mapped[int],
) -> None:
    if task_end_deadline > assignment_end_deadline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task end deadline cannot be later than assignment end deadline.",
        )
