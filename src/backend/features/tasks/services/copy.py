from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.validators import check_admin_permission_in_group
from features.modules.validators import get_module_if_exists
from features.tasks.models import Task
from features.tasks.schemas import TaskRead
from features.tasks.validators import get_task_if_exists
from features.users.validators import check_user_exists


async def copy_task_to_module(
    session: AsyncSession,
    user_id: int,
    source_task_id: int,
    target_module_id: int,
) -> TaskRead:

    await check_user_exists(session=session, user_id=user_id)

    source_task = await get_task_if_exists(
        session=session,
        task_id=source_task_id,
    )
    source_module = await get_module_if_exists(
        session=session, module_id=source_task.module_id
    )

    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=source_module.group_id,
    )

    target_module = await get_module_if_exists(
        session=session, module_id=target_module_id
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=target_module.group_id,
    )

    new_task = Task(
        title=source_task.title,
        description=source_task.description,
        correct_answer=source_task.correct_answer,
        is_active=source_task.is_active,
        module_id=target_module_id,
        max_attempts=source_task.max_attempts,
        start_datetime=source_task.start_datetime,
        end_datetime=source_task.end_datetime,
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return TaskRead(
        id=new_task.id,
        module_id=new_task.module_id,
        group_id=target_module.group_id,
        title=new_task.title,
        description=new_task.description,
        user_answer="",
        is_correct=False,
        user_attempts=0,
        max_attempts=new_task.max_attempts,
        is_active=new_task.is_active,
        start_datetime=new_task.start_datetime,
        end_datetime=new_task.end_datetime,
    )