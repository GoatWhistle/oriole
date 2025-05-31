from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.db_helper import DbHelper
from exceptions.task import (
    check_start_time_not_in_past,
    check_end_time_not_in_past,
    check_end_time_is_after_start_time,
)
from exceptions.user import check_user_exists
from exceptions.assignment import get_assignment_if_exists

from exceptions.group import (
    get_group_if_exists,
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

from utils.time_manager import get_current_utc


async def create_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_in: AssignmentCreate,
) -> AssignmentRead:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=assignment_in.group_id)

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

    await check_start_time_not_in_past(start_datetime=assignment_in.start_datetime)
    await check_end_time_not_in_past(end_datetime=assignment_in.end_datetime)
    await check_end_time_is_after_start_time(
        start_datetime=assignment_in.start_datetime,
        end_datetime=assignment_in.end_datetime,
    )

    assignment = Assignment(
        title=assignment_in.title,
        description=assignment_in.description,
        is_contest=assignment_in.is_contest,
        group_id=assignment_in.group_id,
        admin_id=user_id,
        is_active=assignment_in.start_datetime
        <= get_current_utc()
        <= assignment_in.end_datetime,
        start_datetime=assignment_in.start_datetime,
        end_datetime=assignment_in.end_datetime,
    )

    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)

    return AssignmentRead(
        id=assignment.id,
        group_id=assignment_in.group_id,
        title=assignment_in.title,
        description=assignment_in.description,
        is_contest=assignment_in.is_contest,
        tasks_count=0,
        user_completed_tasks_count=0,
        is_active=assignment.is_active,
        admin_id=assignment.admin_id,
        tasks=[],
        start_datetime=assignment_in.start_datetime,
        end_datetime=assignment_in.end_datetime,
    )


async def get_assignment_by_id(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
) -> AssignmentRead:
    await check_user_exists(session=session, user_id=user_id)
    assignment = await get_assignment_if_exists(
        session=session, assignment_id=assignment_id
    )

    await get_group_if_exists(session=session, group_id=assignment.group_id)
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
        group_id=assignment.group_id,
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
        is_active=assignment.is_active,
        start_datetime=assignment.start_datetime,
        end_datetime=assignment.end_datetime,
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
                is_active=assignment.is_active,
            )
        )

    return assignment_results


async def update_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
    assignment_update: AssignmentUpdate | AssignmentUpdatePartial,
    is_partial: bool = False,
) -> AssignmentRead:
    await check_user_exists(session=session, user_id=user_id)

    assignment = await get_assignment_if_exists(
        session=session, assignment_id=assignment_id
    )

    _ = await get_group_if_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=assignment.group_id
    )

    if "start_datetime" in assignment_update.model_dump(exclude_unset=is_partial):
        await check_start_time_not_in_past(
            start_datetime=assignment_update.start_datetime
        )
        assignment.start_datetime = assignment_update.start_datetime

    if "end_datetime" in assignment_update.model_dump(exclude_unset=is_partial):
        await check_end_time_not_in_past(end_datetime=assignment_update.end_datetime)
        assignment.end_datetime = assignment_update.end_datetime

    await check_end_time_is_after_start_time(
        start_datetime=assignment.start_datetime,
        end_datetime=assignment.end_datetime,
    )

    for name, value in assignment_update.model_dump(exclude_unset=is_partial).items():
        if name not in [
            "start_datetime",
            "end_datetime",
        ]:
            setattr(assignment, name, value)

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

    return AssignmentRead(
        id=assignment.id,
        group_id=assignment.group_id,
        title=assignment.title,
        description=assignment.description,
        is_contest=assignment.is_contest,
        tasks_count=assignment.tasks_count,
        user_completed_tasks_count=user_completed_tasks_count,
        admin_id=assignment.admin_id,
        is_active=assignment.start_datetime
        <= get_current_utc()
        <= assignment.end_datetime,
        start_datetime=assignment.start_datetime,
        end_datetime=assignment.end_datetime,
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


async def delete_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    assignment = await get_assignment_if_exists(
        session=session, assignment_id=assignment_id
    )

    _ = await get_group_if_exists(session=session, group_id=assignment.group_id)
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

    assignment = await get_assignment_if_exists(
        session=session, assignment_id=assignment_id
    )

    _ = await get_group_if_exists(session=session, group_id=assignment.group_id)

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


async def check_assignment_deadlines():
    local_db_helper = DbHelper(
        db_url=str(settings.db.db_url),
    )

    async with local_db_helper.session_factory() as session:
        current_time = get_current_utc()
        result = await session.execute(
            select(Assignment).where(
                (Assignment.start_datetime <= current_time)
                | (Assignment.end_datetime <= current_time)
            )
        )
        assignments = result.scalars().all()

        updated_count = 0
        for assignment in assignments:
            new_status = (
                assignment.start_datetime <= current_time <= assignment.end_datetime
            )
            if assignment.is_active != new_status:
                assignment.is_active = new_status
                updated_count += 1

        if updated_count > 0:
            await session.commit()

        await local_db_helper.dispose()

        return updated_count


async def copy_assignment_to_group(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
    target_group_id: int,
) -> AssignmentRead:
    await check_user_exists(session=session, user_id=user_id)

    source_assignment = await get_assignment_if_exists(
        session=session, assignment_id=assignment_id
    )
    source_group = await get_group_if_exists(
        session=session, group_id=source_assignment.group_id
    )
    _ = await get_group_if_exists(session=session, group_id=target_group_id)

    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=source_group.id,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=target_group_id,
    )

    tasks_query = await session.execute(
        select(Task).where(Task.assignment_id == assignment_id)
    )
    source_tasks = tasks_query.scalars().all()

    new_assignment = Assignment(
        title=source_assignment.title,
        description=source_assignment.description,
        is_contest=source_assignment.is_contest,
        group_id=target_group_id,
        admin_id=user_id,
        is_active=source_assignment.is_active,
        start_datetime=source_assignment.start_datetime,
        end_datetime=source_assignment.end_datetime,
    )

    session.add(new_assignment)
    await session.commit()
    await session.refresh(new_assignment)

    new_tasks = []
    for source_task in source_tasks:
        new_task = Task(
            title=source_task.title,
            description=source_task.description,
            correct_answer=source_task.correct_answer,
            is_active=source_task.is_active,
            assignment_id=new_assignment.id,
            max_attempts=source_task.max_attempts,
            start_datetime=source_task.start_datetime,
            end_datetime=source_task.end_datetime,
        )
        session.add(new_task)
        new_tasks.append(new_task)

    await session.commit()

    for task in new_tasks:
        await session.refresh(task)

    return AssignmentRead(
        id=new_assignment.id,
        group_id=new_assignment.group_id,
        title=new_assignment.title,
        description=new_assignment.description,
        is_contest=new_assignment.is_contest,
        tasks_count=len(new_tasks),
        user_completed_tasks_count=0,
        is_active=new_assignment.is_active,
        admin_id=new_assignment.admin_id,
        tasks=[
            TaskReadPartial(
                id=task.id,
                title=task.title,
                description=task.description,
                is_correct=False,
                is_active=task.is_active,
            )
            for task in new_tasks
        ],
        start_datetime=new_assignment.start_datetime,
        end_datetime=new_assignment.end_datetime,
    )
