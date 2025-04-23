from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.assignment import check_assignment_exists

from core.models import Task, Assignment, Group, Account, UserReply, UserProfile

from core.schemas.task import TaskReadPartial, TaskRead

from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentUpdate,
    AssignmentUpdatePartial,
    AssignmentReadPartial,
)

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)

from core.exceptions.user import check_user_exists


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

    return AssignmentReadPartial.model_validate(assignment)


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
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

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

    return AssignmentRead(
        id=assignment.id,
        title=assignment.title,
        description=assignment.description,
        is_contest=assignment.is_contest,
        admin_id=assignment.admin_id,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=(
                    user_replies.get(task.id, None).is_correct
                    if task.id in user_replies
                    else False
                ),
            )
            for task in tasks
        ],
    )


async def get_user_assignments(
    session: AsyncSession,
    user_id: int,
) -> Sequence[AssignmentReadPartial]:
    await check_user_exists(session=session, user_id=user_id)

    statement_groups = select(Group).join(Account).where(Account.user_id == user_id)
    result_groups: Result = await session.execute(statement_groups)
    groups = result_groups.scalars().all()

    if not groups:
        return []

    group_ids = [group.id for group in groups]
    statement_assignments = select(Assignment).where(Assignment.group_id.in_(group_ids))
    result_assignments: Result = await session.execute(statement_assignments)
    assignments = result_assignments.scalars().all()

    return [
        AssignmentReadPartial.model_validate(assignment.__dict__)
        for assignment in assignments
    ]


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

    return AssignmentReadPartial.model_validate(assignment)


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
