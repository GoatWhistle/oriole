from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import Task
from features.tasks.models import UserReply


async def create_user_reply(
    session: AsyncSession,
    account_id: int,
    task: Task,
    user_answer: str,
) -> UserReply:
    user_reply = UserReply(
        account_id=account_id,
        task_id=task.id,
        user_answer=user_answer,
        is_correct=(user_answer == task.correct_answer),
        user_attempts=1,
    )
    session.add(user_reply)
    await session.commit()
    await session.refresh(user_reply)
    return user_reply


async def get_user_replies(
    session: AsyncSession,
    account_ids: list[int] | None = None,
    task_ids: list[int] | None = None,
) -> list[UserReply]:
    statement = select(UserReply)
    conditions = []
    if account_ids is not None:
        conditions.append(UserReply.account_id.in_(account_ids))
    if task_ids is not None:
        conditions.append(UserReply.task_id.in_(task_ids))
    if conditions:
        statement = statement.where(*conditions)

    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_user_reply_by_account_id_and_task_id(
    session: AsyncSession,
    account_id: int,
    task_id: int,
) -> UserReply | None:
    replies = await get_user_replies(session, [account_id], [task_id])
    return replies[0] if replies else None


async def get_user_replies_by_account_ids_and_task_ids(
    session: AsyncSession,
    account_ids: list[int],
    task_ids: list[int],
) -> list[UserReply]:
    return await get_user_replies(session, account_ids, task_ids)


async def get_user_replies_by_task_ids(
    session: AsyncSession,
    account_id: int,
    task_ids: list[int],
) -> list[UserReply]:
    return await get_user_replies(session, [account_id], task_ids)


async def update_user_reply(
    session: AsyncSession,
    user_reply: UserReply,
    user_answer: str,
    correct_answer: str,
) -> UserReply:
    user_reply.user_answer = user_answer
    user_reply.is_correct = user_answer == correct_answer
    user_reply.user_attempts += 1
    await session.commit()
    await session.refresh(user_reply)
    return user_reply


async def delete_user_reply(
    session: AsyncSession,
    user_reply: UserReply,
) -> None:
    await session.delete(user_reply)
    await session.commit()


async def delete_user_replies_by_task_id(
    session: AsyncSession,
    task_id: int,
) -> None:
    await session.execute(delete(UserReply).where(UserReply.task_id == task_id))
    await session.commit()
