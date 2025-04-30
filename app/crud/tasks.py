from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.user import check_user_exists
from core.exceptions.task import (
    check_task_exists,
    check_counter_limit,
    check_task_is_already_correct,
)
from core.exceptions.assignment import check_assignment_exists

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)

from core.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
    TaskReadPartial,
)

from core.models import (
    Assignment,
    Task,
    Group,
    Account,
    UserReply,
    UserProfile,
)


async def create_task(
    session: AsyncSession,
    user_id: int,
    task_in: TaskCreate,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)

    await check_assignment_exists(session=session, assignment_id=task_in.assignment_id)
    assignment = await session.get(Assignment, task_in.assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)

    await check_user_in_group(
        user_id=user_id,
        group_id=assignment.group_id,
        session=session,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    profile = await session.get(UserProfile, user_id)

    accounts_query = await session.execute(
        select(Account).where(Account.user_id == profile.user_id)
    )
    accounts = accounts_query.scalars().all()

    target_account = None
    for account in accounts:
        if account.group_id == assignment.group_id:
            target_account = account
            break

    task = Task(
        title=task_in.title,
        description=task_in.description,
        assignment_id=task_in.assignment_id,
        correct_answer=task_in.correct_answer,
        max_attempts=task_in.max_attempts,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    user_reply = UserReply(
        account_id=target_account.id,
        task_id=task.id,
        user_answer="",
        is_correct=False,
        user_attempts=0,
    )

    assignment.tasks_count += 1

    session.add(user_reply)
    await session.commit()

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer,
        is_correct=user_reply.is_correct,
        user_attempts=0,
        max_attempts=task.max_attempts,
    )


async def get_task_by_id(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_task_exists(session=session, task_id=task_id)

    task = await session.get(Task, task_id)

    await check_assignment_exists(session=session, assignment_id=task.assignment_id)
    assignment = await session.get(Assignment, task.assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    profile = await session.get(UserProfile, user_id)

    accounts_query = await session.execute(
        select(Account).where(Account.user_id == profile.user_id)
    )
    accounts = accounts_query.scalars().all()

    target_account = None
    for account in accounts:
        if account.group_id == assignment.group_id:
            target_account = account
            break

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == target_account.id, UserReply.task_id == task_id
        )
    )
    user_reply = user_reply_data.scalars().first()

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer if user_reply else "",
        is_correct=user_reply.is_correct if user_reply else False,
        user_attempts=user_reply.user_attempts if user_reply else 0,
        max_attempts=task.max_attempts,
    )


async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
) -> Sequence[TaskReadPartial]:
    await check_user_exists(session=session, user_id=user_id)

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    if not account:
        return []

    statement_groups = select(Group).join(Account).where(Account.user_id == user_id)
    result_groups: Result = await session.execute(statement_groups)
    groups = result_groups.scalars().all()

    if not groups:
        return []

    group_ids = [group.id for group in groups]

    statement_assignments = select(Assignment).where(Assignment.group_id.in_(group_ids))
    result_assignments: Result = await session.execute(statement_assignments)
    assignments = result_assignments.scalars().all()

    if not assignments:
        return []

    assignment_ids = [assignment.id for assignment in assignments]

    statement_tasks = select(Task).where(Task.assignment_id.in_(assignment_ids))
    result_tasks: Result = await session.execute(statement_tasks)
    tasks = result_tasks.scalars().all()

    if not tasks:
        return []

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == account.id,
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )
    user_replies = {reply.task_id: reply for reply in user_reply_data.scalars().all()}

    return [
        TaskReadPartial(
            id=task.id,
            title=task.title,
            description=task.description,
            is_correct=(
                user_replies[task.id].is_correct if task.id in user_replies else False
            ),
        )
        for task in tasks
    ]


async def update_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: TaskUpdate | TaskUpdatePartial,
    is_partial: bool = False,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_task_exists(session=session, task_id=task_id)
    task = await session.get(Task, task_id)

    await check_assignment_exists(session=session, assignment_id=task.assignment_id)
    assignment = await session.get(Assignment, task.assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        user_id=user_id,
        group_id=assignment.group_id,
        session=session,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    for name, value in task_update.model_dump(exclude_unset=is_partial).items():
        setattr(task, name, value)

    await session.commit()
    await session.refresh(task)

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == assignment.group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == account.id, UserReply.task_id == task_id
        )
    )
    user_reply = user_reply_data.scalars().first()

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        user_answer=user_reply.user_answer if user_reply else "",
        is_correct=(
            user_reply.user_answer == task.correct_answer if user_reply else False
        ),
        user_attempts=user_reply.user_attempts if user_reply else 0,
        max_attempts=task.max_attempts,
    )


async def delete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_task_exists(session=session, task_id=task_id)
    task = await session.get(Task, task_id)

    await check_assignment_exists(session=session, assignment_id=task.assignment_id)
    assignment = await session.get(Assignment, task.assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        user_id=user_id,
        group_id=assignment.group_id,
        session=session,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    user_replies_query = await session.execute(
        select(UserReply).where(UserReply.task_id == task_id)
    )
    user_replies = user_replies_query.scalars().all()

    for user_reply in user_replies:
        await session.delete(user_reply)

    await session.delete(task)
    await session.commit()


async def try_to_complete_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    user_answer: str,
) -> TaskRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_task_exists(session=session, task_id=task_id)

    task = await session.get(Task, task_id)
    await check_assignment_exists(session=session, assignment_id=task.assignment_id)

    assignment = await session.get(Assignment, task.assignment_id)
    await check_group_exists(session=session, group_id=assignment.group_id)

    await check_user_in_group(
        user_id=user_id,
        group_id=assignment.group_id,
        session=session,
    )

    profile = await session.get(UserProfile, user_id)

    accounts_query = await session.execute(
        select(Account).where(Account.user_id == profile.user_id)
    )
    accounts = accounts_query.scalars().all()

    target_account = None
    for account in accounts:
        if account.group_id == assignment.group_id:
            target_account = account
            break

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == target_account.id, UserReply.task_id == task_id
        )
    )
    user_reply = user_reply_data.scalars().first()

    if not user_reply:
        user_reply = UserReply(
            account_id=target_account.id,
            task_id=task_id,
            user_answer=user_answer,
            is_correct=(user_answer == task.correct_answer),
        )
        session.add(user_reply)
    else:
        user_reply.user_answer = user_answer
        user_reply.is_correct = user_answer == task.correct_answer

    await session.commit()
    await session.refresh(task)

    await check_task_is_already_correct(
        session=session,
        user_id=user_id,
        user_reply_id=user_reply.id,
        task_id=task_id,
    )
    await check_counter_limit(
        session=session,
        user_id=user_id,
        user_reply_id=user_reply.id,
        task_id=task_id,
    )
    user_reply.user_attempts += 1

    await session.commit()
    await session.refresh(user_reply)

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        is_correct=(user_answer == task.correct_answer),
        user_answer=user_answer,
        user_attempts=user_reply.user_attempts,
        max_attempts=task.max_attempts,
    )
