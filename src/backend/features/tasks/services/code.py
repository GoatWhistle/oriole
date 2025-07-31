from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
import features.tasks.crud.account_task_progress as progress_crud
import features.tasks.crud.base as base_task_crud
import features.tasks.crud.code as task_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    check_user_is_admin_or_owner,
    get_account_or_404,
    get_group_or_404,
)
from features.modules.validators import get_module_or_404
from features.tasks.models import CodeTask
from features.tasks.schemas import (
    CodeTaskCreate,
    CodeTaskRead,
    CodeTaskReadWithProgress,
    CodeTaskUpdate,
)
from features.tasks.validators import (
    get_task_or_404,
    validate_task_deadlines,
)


async def create_code_task(
    session: AsyncSession,
    user_id: int,
    task_in: CodeTaskCreate,
) -> CodeTaskRead:
    module = await get_module_or_404(session, task_in.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    validate_task_deadlines(
        task_in.start_datetime,
        task_in.end_datetime,
        module.start_datetime,
        module.end_datetime,
    )

    task = await task_crud.create_code_task(session, task_in, account.id)
    await module_crud.increment_module_tasks_count(session, module.id)

    return mapper.build_code_task_read_with_progress(cast(CodeTask, task))


async def update_code_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: CodeTaskUpdate,
) -> CodeTaskReadWithProgress:
    task = await get_task_or_404(session, task_id, CodeTask)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = task_update.model_dump(exclude_unset=True)

    updated_start = update_data.get("start_datetime", task.start_datetime)
    updated_end = update_data.get("end_datetime", task.end_datetime)

    validate_task_deadlines(
        updated_start, updated_end, module.start_datetime, module.end_datetime
    )
    task = await base_task_crud.update_task(session, task, update_data)

    account_task_progress = (
        await progress_crud.get_account_task_progress_by_account_and_task_id(
            session, account.id, task.id
        )
    )

    return mapper.build_code_task_read_with_progress(
        cast(CodeTask, task), account_task_progress
    )
