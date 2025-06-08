from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from groups.models import Account
from groups.validators import get_group_if_exists, check_user_in_group
from modules.models import Module
from modules.schemas import ModuleReadPartial
from tasks.models import Task, UserReply
from users.validators import check_user_exists


async def get_modules_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[ModuleReadPartial]:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement = (
        select(
            Module,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.module_id == Module.id)
        .where(Module.group_id == group_id)
        .group_by(Module.id)
        .order_by(Module.id)
    )

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    if not account:
        return []

    result: Result = await session.execute(statement)
    modules = result.all()

    module_results = []
    for module, tasks_count in modules:

        tasks_query = await session.execute(
            select(Task).where(Task.module_id == module.id)
        )
        tasks = tasks_query.scalars().all()

        user_reply_data = await session.execute(
            select(UserReply).where(
                UserReply.account_id == account.id,
                UserReply.task_id.in_([task.id for task in tasks]),
            )
        )

        user_replies = {
            reply.task_id: reply for reply in user_reply_data.scalars().all()
        }

        user_completed_tasks_count = sum(
            1 for reply in user_replies.values() if reply.is_correct
        )

        module_results.append(
            ModuleReadPartial(
                id=module.id,
                title=module.title,
                description=module.description,
                is_contest=module.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
                is_active=module.is_active,
            )
        )

    return module_results
