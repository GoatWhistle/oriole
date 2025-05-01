from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.exceptions.user import check_user_exists
from core.exceptions.assignment import check_assignment_exists

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)

from core.schemas.task import TaskReadPartial

from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentUpdate,
    AssignmentUpdatePartial,
    AssignmentReadPartial,
)

from core.models import (
    Task,
    Assignment,
    Group,
    Account,
    UserReply,
    UserProfile,
)


async def create_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_in: AssignmentCreate,
) -> AssignmentReadPartial:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=assignment_in.group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment_in.group_id,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment_in.group_id,
    )

    assignment = Assignment(**assignment_in.model_dump())
    assignment.admin_id = user_id
    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)

    return AssignmentReadPartial(
        id=assignment.id,
        title=assignment_in.title,
        description=assignment_in.description,
        is_contest=assignment_in.is_contest,
        tasks_count=0,
        user_completed_tasks_count=0,
    )


async def get_assignment_by_id(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
) -> AssignmentRead:
    await check_user_exists(session=session, user_id=user_id)
    await check_assignment_exists(session=session, assignment_id=assignment_id)

    assignment = await session.get(Assignment, assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        session=session, user_id=user_id, group_id=assignment.group_id
    )

    statement = (
        select(
            Assignment,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.assignment_id == Assignment.id)
        .where(Assignment.id == assignment_id)
        .group_by(Assignment.id)
    )

    result: Result = await session.execute(statement)
    assignment_data = result.one_or_none()

    assignment, tasks_count = assignment_data

    tasks_query = await session.execute(
        select(Task).where(Task.assignment_id == assignment_id)
    )
    tasks = tasks_query.scalars().all()

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id == account.id,
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )

    user_replies = {reply.task_id: reply for reply in user_reply_data.scalars().all()}

    user_completed_tasks_count = sum(
        1 for reply in user_replies.values() if reply.is_correct
    )

    return AssignmentRead(
        id=assignment.id,
        title=assignment.title,
        description=assignment.description,
        is_contest=assignment.is_contest,
        admin_id=assignment.admin_id,
        tasks_count=tasks_count,
        user_completed_tasks_count=user_completed_tasks_count,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=user_replies[task.id].is_correct,
                is_active=task.is_active,
            )
            for task in tasks
        ],
    )


async def get_user_assignments(
    session: AsyncSession,
    user_id: int,
) -> Sequence[AssignmentReadPartial]:
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

    statement_assignments = (
        select(
            Assignment,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.assignment_id == Assignment.id)
        .where(Assignment.group_id.in_(group_ids))
        .group_by(Assignment.id)
        .order_by(Assignment.id)
    )

    result_assignments: Result = await session.execute(statement_assignments)
    assignments = result_assignments.all()

    assignment_results = []
    for assignment, tasks_count in assignments:
        tasks_query = await session.execute(
            select(Task).where(Task.assignment_id == assignment.id)
        )
        tasks = tasks_query.scalars().all()

        user_reply_data = await session.execute(
            select(UserReply).where(
                UserReply.account_id == account.id,
                UserReply.task_id.in_([task.id for task in tasks]),
            )
        )

        user_replies = {
            reply.task_id: reply for reply in user_reply_data.scalars().all()
        }

        user_completed_tasks_count = sum(
            1 for reply in user_replies.values() if reply.is_correct
        )

        assignment_results.append(
            AssignmentReadPartial(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                is_contest=assignment.is_contest,
                tasks_count=tasks_count,
                user_completed_tasks_count=user_completed_tasks_count,
            )
        )

    return assignment_results


async def update_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
    assignment_update: AssignmentUpdate | AssignmentUpdatePartial,
    partial: bool = False,
) -> AssignmentReadPartial:
    await check_user_exists(session=session, user_id=user_id)

    await check_assignment_exists(session=session, assignment_id=assignment_id)
    assignment = await session.get(Assignment, assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=assignment.group_id
    )

    for key, value in assignment_update.model_dump(exclude_unset=partial).items():
        setattr(assignment, key, value)

    await session.commit()
    await session.refresh(assignment)

    tasks_query = await session.execute(
        select(Task).where(Task.assignment_id == assignment_id)
    )
    tasks = tasks_query.scalars().all()

    user_replies_query = await session.execute(
        select(UserReply).where(
            UserReply.account_id == user_id,
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )
    user_replies = {
        reply.task_id: reply for reply in user_replies_query.scalars().all()
    }
    user_completed_tasks_count = sum(
        1 for task_id in user_replies if user_replies[task_id].is_correct
    )

    return AssignmentReadPartial(
        id=assignment.id,
        title=assignment.title,
        description=assignment.description,
        is_contest=assignment.is_contest,
        tasks_count=assignment.tasks_count,
        user_completed_tasks_count=user_completed_tasks_count,
    )


async def delete_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_assignment_exists(session=session, assignment_id=assignment_id)
    assignment = await session.get(Assignment, assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=assignment.group_id
    )

    await session.delete(assignment)
    await session.commit()


async def get_tasks_in_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
    is_correct: bool | None,
) -> Sequence[TaskReadPartial]:

    await check_user_exists(session=session, user_id=user_id)

    await check_assignment_exists(session=session, assignment_id=assignment_id)
    assignment = await session.get(Assignment, assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)

    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    statement_tasks = select(Task).where(Task.assignment_id == assignment_id)
    result_tasks: Result = await session.execute(statement_tasks)
    tasks = result_tasks.scalars().all()

    if not tasks:
        return []

    profile = await session.get(UserProfile, user_id)

    accounts_query = await session.execute(
        select(Account).where(Account.user_id == profile.user_id)
    )
    accounts = accounts_query.scalars().all()

    account_ids = {account.id for account in accounts}

    user_reply_data = await session.execute(
        select(UserReply).where(
            UserReply.account_id.in_(account_ids),
            UserReply.task_id.in_([task.id for task in tasks]),
        )
    )
    user_replies = {reply.task_id: reply for reply in user_reply_data.scalars().all()}

    if is_correct is not None:
        tasks = [
            task
            for task in tasks
            if (
                task.id in user_replies
                and user_replies[task.id].is_correct == is_correct
            )
        ]

    return [
        TaskReadPartial(
            id=task.id,
            title=task.title,
            description=task.description,
            is_correct=(
                user_replies[task.id].is_correct if task.id in user_replies else False
            ),
            is_active=task.is_active,
        )
        for task in tasks
    ]
