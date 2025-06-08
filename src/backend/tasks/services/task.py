from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from groups.models import Account, Group
from groups.validators import (
    get_group_if_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)
from modules.models import Module
from modules.validators import get_module_if_exists
from tasks.models import UserReply, Task
from tasks.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
    TaskReadPartial,
)
from tasks.validators import (
    get_task_if_exists,
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
    check_task_start_deadline_before_module_start,
    check_task_end_deadline_after_module_end,
)
from users.models import UserProfile
from users.validators import check_user_exists
from utils import get_current_utc


async def create_task(
    session: AsyncSession,
    user_id: int,
    task_in: TaskCreate,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)

    module = await get_module_if_exists(
        session=session, module_id=task_in.module_id
    )
    _ = await get_group_if_exists(session=session, group_id=module.group_id)

    await check_user_in_group(
        user_id=user_id,
        group_id=module.group_id,
        session=session,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
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

    task = Task(
        title=task_in.title,
        description=task_in.description,
        correct_answer=task_in.correct_answer,
        module_id=task_in.module_id,
        max_attempts=task_in.max_attempts,
        is_active=task_in.start_datetime <= get_current_utc() <= task_in.end_datetime,
        start_datetime=task_in.start_datetime,
        end_datetime=task_in.end_datetime,
    )
    await check_start_time_not_in_past(task=task, start_datetime=task_in.start_datetime)
    await check_end_time_not_in_past(task=task, end_datetime=task_in.end_datetime)

    await check_end_time_is_after_start_time(
        task=task,
        start_datetime=task_in.start_datetime,
        end_datetime=task_in.end_datetime,
    )

    await check_task_start_deadline_before_module_start(
        task=task,
        module=module,
        task_start_deadline=task_in.start_datetime,
        module_start_deadline=module.start_datetime,
    )
    await check_task_end_deadline_after_module_end(
        task=task,
        module=module,
        task_end_deadline=task_in.end_datetime,
        module_end_deadline=module.end_datetime,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    user_reply = UserReply(
        account_id=target_account.id,
        task_id=task.id,
        user_answer="",
        is_correct=False,
        user_attempts=0,
    )

    module.tasks_count += 1

    session.add(user_reply)
    await session.commit()

    return TaskRead(
        id=task.id,
        module_id=task.module_id,
        group_id=module.group_id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer,
        is_correct=user_reply.is_correct,
        user_attempts=0,
        max_attempts=task.max_attempts,
        is_active=task.is_active,
        start_datetime=task_in.start_datetime,
        end_datetime=task_in.end_datetime,
    )


async def get_task_by_id(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)

    task = await get_task_if_exists(session=session, task_id=task_id)
    module = await get_module_if_exists(
        session=session, module_id=task.module_id
    )
    _ = await get_group_if_exists(session=session, group_id=module.group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
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

    return TaskRead(
        id=task.id,
        module_id=task.module_id,
        group_id=module.group_id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer if user_reply else "",
        is_correct=user_reply.is_correct if user_reply else False,
        user_attempts=user_reply.user_attempts if user_reply else 0,
        max_attempts=task.max_attempts,
        is_active=task.is_active,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
    )


async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
    is_correct: bool | None,
) -> Sequence[TaskReadPartial]:
    await check_user_exists(session=session, user_id=user_id)

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    if not account:
        return []

    statement_groups = select(Group).join(Account).where(Account.user_id == user_id)
    result_groups: Result = await session.execute(statement_groups)
    groups = result_groups.scalars().all()

    if not groups:
        return []

    group_ids = [group.id for group in groups]

    statement_modules = select(Module).where(Module.group_id.in_(group_ids))
    result_modules: Result = await session.execute(statement_modules)
    modules = result_modules.scalars().all()

    if not modules:
        return []

    module_ids = [module.id for module in modules]

    statement_tasks = select(Task).where(Task.module_id.in_(module_ids))
    result_tasks: Result = await session.execute(statement_tasks)
    tasks = result_tasks.scalars().all()

    if not tasks:
        return []

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == account.id,
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


async def update_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: TaskUpdate | TaskUpdatePartial,
    is_partial: bool = False,
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
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
    )

    if "start_datetime" in task_update.model_dump(exclude_unset=is_partial):
        await check_start_time_not_in_past(task=task, start_datetime=task_update.start_datetime)
        task.start_datetime = task_update.start_datetime

    if "end_datetime" in task_update.model_dump(exclude_unset=is_partial):
        await check_end_time_not_in_past(task=task, end_datetime=task_update.end_datetime)
        task.end_datetime = task_update.end_datetime

    await check_end_time_is_after_start_time(
        task=task,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
    )

    await check_task_start_deadline_before_module_start(
        task=task,
        module=module,
        task_start_deadline=task.start_datetime,
        module_start_deadline=module.start_datetime,
    )
    await check_task_end_deadline_after_module_end(
        task=task,
        module=module,
        task_end_deadline=task.end_datetime,
        module_end_deadline=module.end_datetime,
    )

    for name, value in task_update.model_dump(exclude_unset=is_partial).items():
        if name not in [
            "start_datetime",
            "end_datetime",
        ]:
            setattr(task, name, value)

    await session.commit()
    await session.refresh(task)

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == module.group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == account.id, UserReply.task_id == task_id
        )
    )
    user_reply = user_reply_data.scalars().first()

    return TaskRead(
        id=task.id,
        module_id=task.module_id,
        group_id=module.group_id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer if user_reply else "",
        is_correct=(
            user_reply.user_answer == task.correct_answer if user_reply else False
        ),
        user_attempts=user_reply.user_attempts if user_reply else 0,
        max_attempts=task.max_attempts,
        is_active=task.start_datetime <= get_current_utc() <= task.end_datetime,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
    )


async def delete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> None:
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
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
    )

    user_replies_query = await session.execute(
        select(UserReply).where(UserReply.task_id == task_id)
    )
    user_replies = user_replies_query.scalars().all()

    for user_reply in user_replies:
        await session.delete(user_reply)

    await session.delete(task)
    await session.commit()