from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
import features.tasks.crud.account_task_progress as progress_crud
import features.tasks.crud.base as base_task_crud
import features.tasks.crud.string_match as task_crud
import features.tasks.mappers as mapper
from features.groups.validators import check_user_is_admin_or_owner, get_account_or_404
from features.modules.validators import get_module_or_404
from features.spaces.validators import get_space_or_404
from features.tasks.models import StringMatchTask
from features.tasks.schemas import (
    StringMatchTaskCreate,
    StringMatchTaskRead,
    StringMatchTaskUpdate,
)
from features.tasks.schemas import StringMatchTaskReadWithProgress
from features.tasks.validators import (
    get_task_or_404,
    validate_string_match_task_configuration,
    validate_task_deadlines,
)


async def create_string_match_task(
    session: AsyncSession,
    user_id: int,
    task_in: StringMatchTaskCreate,
) -> StringMatchTaskRead:
    module = await get_module_or_404(session, task_in.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    validate_task_deadlines(
        task_in.start_datetime,
        task_in.end_datetime,
        module.start_datetime,
        module.end_datetime,
    )
    validate_string_match_task_configuration(task_in)
    task = await task_crud.create_string_match_task(session, task_in, account.id)
    await module_crud.increment_module_tasks_count(session, module.id)

    return mapper.build_string_match_task_read_with_correctness(
        cast(StringMatchTask, task)
    )


async def update_string_match_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: StringMatchTaskUpdate,
) -> StringMatchTaskReadWithProgress:
    task = await get_task_or_404(session, task_id, StringMatchTask)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = task_update.model_dump(exclude_unset=True)

    updated_start = update_data.get("start_datetime", task.start_datetime)
    updated_end = update_data.get("end_datetime", task.end_datetime)
    validate_task_deadlines(
        updated_start, updated_end, module.start_datetime, module.end_datetime
    )
    if (
        "compare_as_number" in update_data
        and "is_case_sensitive" in update_data
        and "normalize_whitespace" in update_data
    ):
        validate_string_match_task_configuration(update_data)
    task = await base_task_crud.update_task(session, task, update_data)

    account_task_progress = (
        await progress_crud.get_account_task_progress_by_account_id_and_task_id(
            session, account.id, task_id
        )
    )

    return mapper.build_string_match_task_read_with_correctness(
        cast(StringMatchTask, task), account_task_progress
    )
