from typing import Sequence

from sqlalchemy import select, func, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import Account, Group
from features.groups.validators import (
    get_group_if_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)
from features.modules.models import Module
from features.modules.schemas import (
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
    ModuleUpdatePartial,
    ModuleReadPartial,
)
from features.modules.validators import get_module_if_exists
from features.tasks.models import Task, UserReply
from features.tasks.schemas import TaskReadPartial
from features.tasks.validators import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
)
from features.users.validators import check_user_exists
from utils import get_current_utc


async def create_module(
    session: AsyncSession,
    user_id: int,
    module_in: ModuleCreate,
) -> ModuleRead:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=module_in.group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=module_in.group_id,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=module_in.group_id,
    )

    await check_start_time_not_in_past(start_datetime=module_in.start_datetime)
    await check_end_time_not_in_past(end_datetime=module_in.end_datetime)
    await check_end_time_is_after_start_time(
        start_datetime=module_in.start_datetime,
        end_datetime=module_in.end_datetime,
    )

    module = Module(
        title=module_in.title,
        description=module_in.description,
        is_contest=module_in.is_contest,
        group_id=module_in.group_id,
        admin_id=user_id,
        is_active=module_in.start_datetime
        <= get_current_utc()
        <= module_in.end_datetime,
        start_datetime=module_in.start_datetime,
        end_datetime=module_in.end_datetime,
    )

    session.add(module)
    await session.commit()
    await session.refresh(module)

    return ModuleRead(
        id=module.id,
        group_id=module_in.group_id,
        title=module_in.title,
        description=module_in.description,
        is_contest=module_in.is_contest,
        tasks_count=0,
        user_completed_tasks_count=0,
        is_active=module.is_active,
        admin_id=module.admin_id,
        tasks=[],
        start_datetime=module_in.start_datetime,
        end_datetime=module_in.end_datetime,
    )


async def get_module_by_id(
    session: AsyncSession,
    user_id: int,
    module_id: int,
) -> ModuleRead:
    await check_user_exists(session=session, user_id=user_id)
    module = await get_module_if_exists(session=session, module_id=module_id)

    await get_group_if_exists(session=session, group_id=module.group_id)
    await check_user_in_group(
        session=session, user_id=user_id, group_id=module.group_id
    )

    statement = (
        select(
            Module,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.module_id == Module.id)
        .where(Module.id == module_id)
        .group_by(Module.id)
    )

    result: Result = await session.execute(statement)
    module_data = result.one_or_none()

    module, tasks_count = module_data

    tasks_query = await session.execute(select(Task).where(Task.module_id == module_id))
    tasks = tasks_query.scalars().all()

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == account.id,
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )

    user_replies = {reply.task_id: reply for reply in user_reply_data.scalars().all()}

    user_completed_tasks_count = sum(
        1 for reply in user_replies.values() if reply.is_correct
    )

    return ModuleRead(
        id=module.id,
        group_id=module.group_id,
        title=module.title,
        description=module.description,
        is_contest=module.is_contest,
        admin_id=module.admin_id,
        tasks_count=tasks_count,
        user_completed_tasks_count=user_completed_tasks_count,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=user_replies[task.id].is_correct,
                is_active=task.is_active,
            )
            for task in tasks
        ],
        is_active=module.is_active,
        start_datetime=module.start_datetime,
        end_datetime=module.end_datetime,
    )


async def get_user_modules(
    session: AsyncSession,
    user_id: int,
) -> Sequence[ModuleReadPartial]:
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

    statement_modules = (
        select(
            Module,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.module_id == Module.id)
        .where(Module.group_id.in_(group_ids))
        .group_by(Module.id)
        .order_by(Module.id)
    )

    result_modules: Result = await session.execute(statement_modules)
    modules = result_modules.all()

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


async def update_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    module_update: ModuleUpdate | ModuleUpdatePartial,
    is_partial: bool = False,
) -> ModuleRead:
    await check_user_exists(session=session, user_id=user_id)

    module = await get_module_if_exists(session=session, module_id=module_id)

    _ = await get_group_if_exists(session=session, group_id=module.group_id)
    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
    )
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=module.group_id
    )

    if "start_datetime" in module_update.model_dump(exclude_unset=is_partial):
        await check_start_time_not_in_past(start_datetime=module_update.start_datetime)
        module.start_datetime = module_update.start_datetime

    if "end_datetime" in module_update.model_dump(exclude_unset=is_partial):
        await check_end_time_not_in_past(end_datetime=module_update.end_datetime)
        module.end_datetime = module_update.end_datetime

    await check_end_time_is_after_start_time(
        start_datetime=module.start_datetime,
        end_datetime=module.end_datetime,
    )

    for name, value in module_update.model_dump(exclude_unset=is_partial).items():
        if name not in [
            "start_datetime",
            "end_datetime",
        ]:
            setattr(module, name, value)

    await session.commit()
    await session.refresh(module)

    tasks_query = await session.execute(select(Task).where(Task.module_id == module_id))
    tasks = tasks_query.scalars().all()

    user_replies_query = await session.execute(
        select(UserReply).where(
            UserReply.account_id == user_id,
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )
    user_replies = {
        reply.task_id: reply for reply in user_replies_query.scalars().all()
    }
    user_completed_tasks_count = sum(
        1 for task_id in user_replies if user_replies[task_id].is_correct
    )

    return ModuleRead(
        id=module.id,
        group_id=module.group_id,
        title=module.title,
        description=module.description,
        is_contest=module.is_contest,
        tasks_count=module.tasks_count,
        user_completed_tasks_count=user_completed_tasks_count,
        admin_id=module.admin_id,
        is_active=module.start_datetime <= get_current_utc() <= module.end_datetime,
        start_datetime=module.start_datetime,
        end_datetime=module.end_datetime,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=user_replies[task.id].is_correct,
                is_active=task.is_active,
            )
            for task in tasks
        ],
    )


async def delete_module(
    session: AsyncSession,
    user_id: int,
    module_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)

    module = await get_module_if_exists(session=session, module_id=module_id)

    await get_group_if_exists(session=session, group_id=module.group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=module.group_id,
    )

    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=module.group_id
    )

    tasks_query = await session.execute(select(Task).where(Task.module_id == module_id))
    tasks = tasks_query.scalars().all()

    task_ids = [task.id for task in tasks]
    if task_ids:
        await session.execute(delete(UserReply).where(UserReply.task_id.in_(task_ids)))

    for task in tasks:
        await session.delete(task)

    await session.delete(module)
    await session.commit()
