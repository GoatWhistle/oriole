from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
import features.modules.mappers as mapper
import features.tasks.crud.task as task_crud
from features.groups.validators import (
    get_group_if_exists,
    get_account_if_exists,
    check_user_is_admin_or_owner,
)
from features.modules.schemas import ModuleRead, ModuleCreate
from features.modules.validators import get_module_if_exists
from features.users.validators import check_user_exists


async def copy_module_to_group(
    session: AsyncSession,
    user_id: int,
    module_id: int,
    target_group_id: int,
) -> ModuleRead:
    await check_user_exists(session, user_id)

    module = await get_module_if_exists(session, module_id)

    _ = await get_group_if_exists(session, module.group_id)
    source_account = await get_account_if_exists(session, user_id, module.group_id)

    check_user_is_admin_or_owner(source_account.role, user_id)

    if module.group_id != target_group_id:
        _ = await get_group_if_exists(session, target_group_id)
        target_account = await get_account_if_exists(session, user_id, target_group_id)

        check_user_is_admin_or_owner(target_account.role, user_id)

    source_tasks = await task_crud.get_tasks_by_module_id(session, module_id)

    module_create = ModuleCreate(
        title=module.title,
        description=module.description,
        is_contest=module.is_contest,
        group_id=target_group_id,
        start_datetime=module.start_datetime,
        end_datetime=module.end_datetime,
    )
    new_module = await module_crud.create_module(session, module_create, user_id)
    new_tasks = await task_crud.clone_tasks_to_module(
        session, source_tasks, new_module.id
    )

    return mapper.build_module_read(new_module, target_group_id, new_tasks)
