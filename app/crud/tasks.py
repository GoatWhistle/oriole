from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Assignment, Task

from core.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
)
from core.exceptions.user import check_user_exists
from core.exceptions.task import check_task_exists
from core.exceptions.assignment import check_assignment_exists

from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
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
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=assignment.group_id,
    )

    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskRead.model_validate(task)


async def get_task(
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

    return TaskRead.model_validate(task)


async def get_tasks(
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


async def update_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    task_update: TaskUpdate | TaskUpdatePartial,
    partial: bool = False,
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
    for name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, name, value)

    await session.commit()
    await session.refresh(task)

    return TaskRead.model_validate(task)


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

    await session.delete(task)
    await session.commit()
