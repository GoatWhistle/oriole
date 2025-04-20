from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.assignment import check_assignment_exists

from core.models import Task, Assignment

from core.schemas.task import TaskRead

from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentUpdate,
    AssignmentUpdatePartial,
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
) -> AssignmentRead:
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
    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)

    return AssignmentRead.model_validate(assignment)


async def get_assignment(
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

    return AssignmentRead.model_validate(assignment)


async def get_assignments(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Sequence[AssignmentRead]:
    await check_user_exists(session=session, user_id=user_id)
    await check_group_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement = (
        select(Assignment)
        .where(Assignment.group_id == group_id)
        .order_by(Assignment.id)
    )

    result: Result = await session.execute(statement)
    assignments = list(result.scalars().all())

    return [AssignmentRead.model_validate(assignment) for assignment in assignments]


async def update_assignment(
    session: AsyncSession,
    user_id: int,
    assignment_id: int,
    assignment_update: AssignmentUpdate | AssignmentUpdatePartial,
    partial: bool = False,
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
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=assignment.group_id
    )

    for name, value in assignment_update.model_dump(exclude_unset=partial).items():
        setattr(assignment, name, value)

    await session.commit()
    await session.refresh(assignment)

    return AssignmentRead.model_validate(assignment)


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
) -> Sequence[TaskRead]:
    await check_user_exists(session=session, user_id=user_id)
    await check_assignment_exists(session=session, assignment_id=assignment_id)
    assignment = await session.get(Assignment, assignment_id)

    await check_group_exists(session=session, group_id=assignment.group_id)
    await check_user_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    statement = (
        select(Task).where(Task.assignment_id == assignment_id).order_by(Task.id)
    )

    result: Result = await session.execute(statement)
    tasks = list(result.scalars().all())

    return [TaskRead.model_validate(task) for task in tasks]
