from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.task as task_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    get_group_if_exists,
    check_user_is_admin_or_owner,
    get_account_if_exists,
)
from features.modules.validators import get_module_if_exists
from features.tasks.schemas import TaskCreate
from features.tasks.schemas import TaskRead
from features.tasks.validators import get_task_if_exists
from features.users.validators import check_user_exists


async def copy_task_to_module(
    session: AsyncSession,
    user_id: int,
    source_task_id: int,
    target_module_id: int,
) -> TaskRead:
    await check_user_exists(session, user_id)

    task = await get_task_if_exists(session, source_task_id)

    source_module = await get_module_if_exists(session, task.module_id)
    source_group = await get_group_if_exists(session, source_module.group_id)
    source_account = await get_account_if_exists(
        session, user_id, source_module.group_id
    )

    check_user_is_admin_or_owner(source_account.role, user_id)

    target_module = (
        await get_module_if_exists(session, target_module_id)
        if source_module.id != target_module_id
        else source_module
    )

    if source_module.group_id != target_module.group_id:
        target_group = await get_group_if_exists(session, target_module.group_id)
        target_account = await get_account_if_exists(session, user_id, target_group.id)
        check_user_is_admin_or_owner(target_account.role, user_id)
    else:
        target_group = source_group

    task_create = TaskCreate(
        title=task.title,
        description=task.description,
        correct_answer=task.correct_answer,
        module_id=target_module_id,
        max_attempts=task.max_attempts,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
    )
    new_task = await task_crud.create_task(session, task_create)

    return mapper.build_task_read(new_task, target_group.id)
