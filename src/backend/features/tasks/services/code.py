from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
import features.solutions.crud.base as solution_crud
import features.tasks.crud.base as base_task_crud
import features.tasks.crud.code as task_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.validators import get_module_or_404
from features.solutions.models import CodeSolution
from features.tasks.models import CodeTask
from features.tasks.schemas import (
    CodeTaskCreate,
    CodeTaskRead,
    CodeTaskUpdate,
    CodeTaskReadWithCorrectness,
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

    task = await task_crud.create_code_task(session, task_in, user_id)
    await module_crud.increment_module_tasks_count(session, module.id)

    return task.get_validation_schema()


async def update_code_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: CodeTaskUpdate,
) -> CodeTaskReadWithCorrectness:
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
    solutions = await solution_crud.get_solutions_by_account_id_and_task_id(
        session, account.id, task_id
    )

    return mapper.build_code_task_read_with_correctness(
        cast(CodeTask, task),
        cast(list[CodeSolution], solutions),
    )
