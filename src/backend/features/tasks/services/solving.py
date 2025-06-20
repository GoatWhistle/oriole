from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.user_reply as user_reply_crud
import features.tasks.mappers as mapper
from features.groups.validators import get_group_if_exists, get_account_if_exists
from features.modules.validators import get_module_if_exists
from features.tasks.schemas import TaskRead
from features.tasks.validators import (
    get_task_if_exists,
    check_counter_limit,
    check_task_is_already_correct,
)
from features.users.validators import check_user_exists
from validators import check_deadline_not_passed


async def try_to_complete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    user_answer: str,
) -> TaskRead:
    await check_user_exists(session, user_id)

    task = await get_task_if_exists(session, task_id)
    module = await get_module_if_exists(session, task.module_id)
    _ = await get_group_if_exists(session, module.group_id)
    account = await get_account_if_exists(session, user_id, module.group_id)

    check_deadline_not_passed(task)

    user_reply = await user_reply_crud.get_user_reply_by_account_id_and_task_id(
        session, account.id, task_id
    )
    if user_reply:
        check_task_is_already_correct(user_id, task_id, user_reply.is_correct)
        check_counter_limit(
            user_id, task_id, task.max_attempts, user_reply.user_attempts
        )
        user_reply = await user_reply_crud.update_user_reply(
            session, user_reply, user_answer, task.correct_answer
        )
    else:
        user_reply = await user_reply_crud.create_user_reply(
            session, account.id, task, user_answer
        )

    return mapper.build_task_read(task, module.group_id, user_reply)
