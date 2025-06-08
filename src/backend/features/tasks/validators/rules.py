from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from features.tasks.models import Task, UserReply


async def check_counter_limit(
    session: AsyncSession,
    user_id: int | Mapped[int],
    user_reply_id: int | Mapped[int],
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
    user_id: int | Mapped[int],
    user_reply_id: int | Mapped[int],
    task: Task,
) -> None:
    user_reply = await session.get(UserReply, user_reply_id)

    if user_reply and user_reply.is_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Task {task.id} has already been solved correctly by user {user_id}.",
        )
