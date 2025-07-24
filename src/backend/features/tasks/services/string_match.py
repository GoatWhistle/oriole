from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
import features.solutions.crud.base as solution_crud
import features.tasks.crud.base as base_task_crud
import features.tasks.crud.string_match as task_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.validators import get_module_or_404
from features.solutions.models import StringMatchSolution
from features.spaces.validators import get_space_or_404
from features.tasks.models import StringMatchTask
from features.tasks.schemas import (
    StringMatchTaskCreate,
    StringMatchTaskRead,
    StringMatchTaskUpdate,
)
from features.tasks.schemas import StringMatchTaskReadWithCorrectness
from features.tasks.validators import (
    get_task_or_404,
    validate_task_deadlines,
    validate_string_match_task_configuration,
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

    return task.get_validation_schema()


async def update_string_match_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: StringMatchTaskUpdate,
) -> StringMatchTaskReadWithCorrectness:
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
    validate_string_match_task_configuration(task_update)
    task = await base_task_crud.update_task(session, task, update_data)

    solutions = await solution_crud.get_solutions_by_account_id_and_task_id(
        session, account.id, task_id
    )

    return mapper.build_string_match_task_read_with_correctness(
        cast(StringMatchTask, task),
        cast(list[StringMatchSolution], solutions),
    )
