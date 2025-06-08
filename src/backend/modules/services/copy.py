from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from groups.validators import get_group_if_exists, check_admin_permission_in_group
from modules.models import Module
from modules.schemas import ModuleRead
from modules.validators import get_module_if_exists
from tasks.models import Task
from tasks.schemas import TaskReadPartial
from users.validators import check_user_exists


async def copy_module_to_group(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    target_group_id: int,
) -> ModuleRead:
    await check_user_exists(session=session, user_id=user_id)

    source_module = await get_module_if_exists(
        session=session, module_id=module_id
    )
    source_group = await get_group_if_exists(
        session=session, group_id=source_module.group_id
    )
    _ = await get_group_if_exists(session=session, group_id=target_group_id)

    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=source_group.id,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=target_group_id,
    )

    tasks_query = await session.execute(
        select(Task).where(Task.module_id == module_id)
    )
    source_tasks = tasks_query.scalars().all()

    new_module = Module(
        title=source_module.title,
        description=source_module.description,
        is_contest=source_module.is_contest,
        group_id=target_group_id,
        admin_id=user_id,
        is_active=source_module.is_active,
        start_datetime=source_module.start_datetime,
        end_datetime=source_module.end_datetime,
    )

    session.add(new_module)
    await session.commit()
    await session.refresh(new_module)

    new_tasks = []
    for source_task in source_tasks:
        new_task = Task(
            title=source_task.title,
            description=source_task.description,
            correct_answer=source_task.correct_answer,
            is_active=source_task.is_active,
            module_id=new_module.id,
            max_attempts=source_task.max_attempts,
            start_datetime=source_task.start_datetime,
            end_datetime=source_task.end_datetime,
        )
        session.add(new_task)
        new_tasks.append(new_task)

    await session.commit()

    for task in new_tasks:
        await session.refresh(task)

    return ModuleRead(
        id=new_module.id,
        group_id=new_module.group_id,
        title=new_module.title,
        description=new_module.description,
        is_contest=new_module.is_contest,
        tasks_count=len(new_tasks),
        user_completed_tasks_count=0,
        is_active=new_module.is_active,
        admin_id=new_module.admin_id,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=False,
                is_active=task.is_active,
            )
            for task in new_tasks
        ],
        start_datetime=new_module.start_datetime,
        end_datetime=new_module.end_datetime,
    )