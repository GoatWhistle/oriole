from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from groups.models import Account
from groups.validators import get_group_if_exists, check_user_in_group
from modules.validators import get_module_if_exists
from tasks.models import Task, UserReply
from tasks.schemas import TaskReadPartial
from users.models import UserProfile
from users.validators import check_user_exists


async def get_tasks_in_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    is_correct: bool | None,
) -> Sequence[TaskReadPartial]:

    await check_user_exists(session=session, user_id=user_id)

    module = await get_module_if_exists(session=session, module_id=module_id)

    _ = await get_group_if_exists(session=session, group_id=module.group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
    )

    statement_tasks = select(Task).where(Task.module_id == module_id)
    result_tasks: Result = await session.execute(statement_tasks)
    tasks = result_tasks.scalars().all()

    if not tasks:
        return []

    profile = await session.get(UserProfile, user_id)

    accounts_query = await session.execute(
        select(Account).where(Account.user_id == profile.user_id)
    )
    accounts = accounts_query.scalars().all()

    account_ids = {account.id for account in accounts}

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id.in_(account_ids),
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )
    user_replies = {reply.task_id: reply for reply in user_reply_data.scalars().all()}

    if is_correct is not None:
        tasks = [
            task
            for task in tasks
            if (
                task.id in user_replies
                and user_replies[task.id].is_correct == is_correct
            )
        ]

    return [
        TaskReadPartial(
            id=task.id,
            title=task.title,
            description=task.description,
            is_correct=(
                user_replies[task.id].is_correct if task.id in user_replies else False
            ),
            is_active=task.is_active,
        )
        for task in tasks
    ]
