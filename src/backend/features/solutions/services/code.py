from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.crud.code as code_solution_crud
import features.tasks.crud.test as test_crud
from core.celery.app import app as celery_app
from features import StringMatchTask
from features.groups.validators import get_group_or_404, get_account_or_404
from features.modules.validators import get_module_or_404
from features.tasks.validators import get_task_or_404
from shared.validators import check_is_active


async def create_code_solution(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    code: str,
) -> dict:
    task = cast(
        StringMatchTask, await get_task_or_404(session, task_id, StringMatchTask)
    )
    module = await get_module_or_404(session, task.module_id)
    group = await get_group_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)
    tests = await test_crud.get_tests(session, task.id)

    check_is_active(task.is_active)

    solution = await code_solution_crud.create_solution()
    result = await celery_app.check_code(group, account, tests)

    # += 1 current_attemps

    if result.is_coorect:
        pass  # is_correct
    return result


async def get_task_by_id(
    session,
    user_id,
    solution_id,
):
    pass


async def get_user_tasks(
    session,
    user_id,
):
    pass
