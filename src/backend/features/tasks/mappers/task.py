from features.modules.models import Module
from features.tasks.models import Task, UserReply
from features.tasks.schemas import TaskRead
from features.tasks.schemas.task import TaskReadWithoutReplies


def build_task_read(
    task: Task,
    module: Module,
    user_reply: UserReply | None = None,
) -> TaskRead | TaskReadWithoutReplies:
    if user_reply:
        return TaskRead(
            title=task.title,
            description=task.description,
            start_datetime=task.start_datetime,
            end_datetime=task.end_datetime,
            max_attempts=task.max_attempts,
            id=task.id,
            is_correct=user_reply.is_correct if user_reply else False,
            is_active=task.is_active,
            module_id=task.module_id,
            group_id=module.group_id,
            user_answer=user_reply.user_answer if user_reply else "",
            user_attempts=user_reply.user_attempts if user_reply else 0,
        )
    return TaskReadWithoutReplies(
        title=task.title,
        description=task.description,
        start_datetime=task.start_datetime,
        end_datetime=task.end_datetime,
        max_attempts=task.max_attempts,
        id=task.id,
        is_active=task.is_active,
        module_id=task.module_id,
        group_id=module.group_id,
        is_correct=False,
    )


def build_task_read_list(
    modules: list[Module],
    tasks: list[Task],
    user_replies: list[UserReply],
) -> list[TaskRead]:
    module_by_id = {module.id: module for module in modules}
    user_replies_by_task_id = {reply.task_id: reply for reply in user_replies}

    return [
        build_task_read(
            task=task,
            module=module_by_id[task.module_id],
            user_reply=user_replies_by_task_id.get(task.id),
        )
        for task in tasks
        if task.module_id in module_by_id
    ]
