from typing import Sequence

from features.tasks.models import Task, UserReply
from features.tasks.schemas import TaskRead, TaskReadPartial


def build_task_read(
    task: Task,
    group_id: int,
    user_reply: UserReply | None = None,
) -> TaskRead:
    return TaskRead(
        id=task.id,
        module_id=task.module_id,
        group_id=group_id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer if user_reply else "",
        is_correct=(
            user_reply.user_answer == task.correct_answer if user_reply else False
        ),
        user_attempts=user_reply.user_attempts if user_reply else 0,
        max_attempts=task.max_attempts,
        is_active=task.is_active,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
    )


def build_task_read_partial(
    task: Task,
    user_reply: UserReply | None = None,
) -> TaskReadPartial:
    return TaskReadPartial(
        id=task.id,
        title=task.title,
        description=task.description,
        is_correct=user_reply.is_correct if user_reply else False,
        is_active=task.is_active,
    )


def build_task_read_partial_list(
    tasks: Sequence[Task],
    user_replies: Sequence[UserReply],
) -> Sequence[TaskReadPartial]:
    user_replies_by_task_id = {reply.task_id: reply for reply in user_replies}

    return [
        build_task_read_partial(task, user_replies_by_task_id.get(task.id))
        for task in tasks
    ]
