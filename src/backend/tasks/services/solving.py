from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from groups.models import Account
from groups.validators import get_group_if_exists, check_user_in_group
from modules.validators import get_module_if_exists
from tasks.models import UserReply
from tasks.schemas import TaskRead
from tasks.validators import (
    get_task_if_exists,
    check_counter_limit,
    check_task_is_already_correct,
    check_deadline_not_passed,
)
from users.models import UserProfile
from users.validators import check_user_exists
from utils import get_current_utc


async def try_to_complete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    user_answer: str,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)

    task = await get_task_if_exists(session=session, task_id=task_id)
    module = await get_module_if_exists(
        session=session, module_id=task.module_id
    )
    _ = await get_group_if_exists(session=session, group_id=module.group_id)

    await check_user_in_group(
        user_id=user_id,
        group_id=module.group_id,
        session=session,
    )

    profile = await session.get(UserProfile, user_id)

    accounts_query = await session.execute(
        select(Account).where(Account.user_id == profile.user_id)
    )
    accounts = accounts_query.scalars().all()

    target_account = None
    for account in accounts:
        if account.group_id == module.group_id:
            target_account = account
            break

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == target_account.id, UserReply.task_id == task_id
        )
    )
    user_reply = user_reply_data.scalars().first()

    if not user_reply:
        user_reply = UserReply(
            account_id=target_account.id,
            task_id=task_id,
            user_answer=user_answer,
            is_correct=(user_answer == task.correct_answer),
        )
        session.add(user_reply)
    else:
        user_reply.user_answer = user_answer
        user_reply.is_correct = user_answer == task.correct_answer

    user_reply.user_attempts += 1

    await session.commit()
    await session.refresh(task)

    await check_task_is_already_correct(
        session=session,
        user_id=user_id,
        user_reply_id=user_reply.id,
        task=task,
    )
    await check_deadline_not_passed(task=task)
    await check_counter_limit(
        session=session,
        user_id=user_id,
        user_reply_id=user_reply.id,
        task=task,
    )
    user_reply.user_attempts += 1

    await session.commit()
    await session.refresh(user_reply)

    return TaskRead(
        id=task.id,
        module_id=task.module_id,
        group_id=module.group_id,
        title=task.title,
        description=task.description,
        is_correct=(user_answer == task.correct_answer),
        user_answer=user_answer,
        user_attempts=user_reply.user_attempts,
        max_attempts=task.max_attempts,
        is_active=task.start_datetime <= get_current_utc() <= task.end_datetime,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
    )
