from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
import features.tasks.crud.base as base_task_crud
import features.tasks.crud.code as task_crud
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.validators import get_module_or_404
from features.tasks.schemas import (
    CodeTaskCreate,
    CodeTaskRead,
    CodeTaskUpdate,
    CodeTaskUpdatePartial,
)
from features.tasks.validators import (
    get_task_or_404,
    check_task_start_deadline_after_module_start,
    check_task_end_deadline_before_module_end,
)
from shared.validators import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
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

    check_start_time_not_in_past(task_in.start_datetime)
    check_end_time_not_in_past(task_in.end_datetime)
    check_end_time_is_after_start_time(task_in.start_datetime, task_in.end_datetime)
    check_task_start_deadline_after_module_start(
        task_in.start_datetime, module.start_datetime
    )
    check_task_end_deadline_before_module_end(task_in.end_datetime, module.end_datetime)

    task = await task_crud.create_code_task(session, task_in)
    await module_crud.increment_module_tasks_count(session, module.id)

    return task.get_validation_schema()


async def update_code_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: CodeTaskUpdate | CodeTaskUpdatePartial,
    is_partial: bool = False,
) -> CodeTaskRead:
    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = task_update.model_dump(exclude_unset=is_partial)

    if "start_datetime" in update_data:
        check_start_time_not_in_past(update_data["start_datetime"])
    if "end_datetime" in update_data:
        check_end_time_not_in_past(update_data["end_datetime"])

    if "start_datetime" in update_data or "end_datetime" in update_data:
        start = update_data.get("start_datetime", task.start_datetime)
        end = update_data.get("end_datetime", task.end_datetime)
        check_end_time_is_after_start_time(start, end)

    check_task_start_deadline_after_module_start(
        task.start_datetime, module.start_datetime
    )
    check_task_end_deadline_before_module_end(task.end_datetime, module.end_datetime)

    task = await base_task_crud.update_task(session, task, update_data)

    return task.get_validation_schema()
