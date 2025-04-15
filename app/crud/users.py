from typing import Sequence
from sqlalchemy import select, and_
from sqlalchemy.engine import Result

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Group, Task, Account, Assignment
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead
from core.schemas.assignment import AssignmentRead

from core.exceptions.user import (
    get_user_or_404_with_return,
    check_teacher_or_403,
)
from core.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> UserRead:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    user = await get_user_or_404_with_return(session=session, user_id=user_id)
    return UserRead.model_validate(user)


async def update_user(
    session: AsyncSession,
    user_id: int,
    user_update: UserUpdate,
    partial: bool = False,
) -> UserRead:
    user = await get_user_or_404_with_return(session, user_id)

    for key, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


async def delete_user(
    session: AsyncSession,
    user_id: int,
) -> None:
    user = await get_user_or_404_with_return(session, user_id)
    await session.delete(user)
    await session.commit()


async def get_user_groups(
    session: AsyncSession,
    user_id: int,
) -> Sequence[GroupRead]:
    statement = (
        select(Group).join(Account).where(Account.user_id == user_id).order_by(Group.id)
    )

    result: Result = await session.execute(statement)
    groups = result.scalars().all()

    return [GroupRead.model_validate(group) for group in groups]


async def get_user_assignments(
    session: AsyncSession,
    user_id: int,
) -> Sequence[AssignmentRead]:
    statement = (
        select(Assignment)
        .join(Group)
        .join(Account)
        .where(and_(Account.user_id == user_id, Assignment.group_id == Group.id))
        .order_by(Assignment.id)
    )

    result = await session.execute(statement)
    assignments = result.scalars().all()

    return [AssignmentRead.model_validate(assignment) for assignment in assignments]


async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
) -> Sequence[TaskRead]:
    statement = (
        select(Task)
        .join(Group)
        .join(Account)
        .where(
            and_(
                Account.user_id == user_id,
                Task.assignment_id == Assignment.id,
            )
        )
        .order_by(Task.id)
    )

    result = await session.execute(statement)
    tasks = result.scalars().all()

    return [TaskRead.model_validate(task) for task in tasks]


async def add_user_to_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    current_user: User,
) -> None:
    user = await get_user_or_404_with_return(session, user_id)
    user = await check_teacher_or_403(session, user_id)

    existing = await session.execute(
        select(Account).where(
            (Account.user_id == user_id) & (Account.group_id == group_id)
        )
    )
    # if existing.scalar_one_or_none():
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT, detail="User already in this group"
    #     )

    account = Account(user_id=user_id, group_id=group_id)
    session.add(account)
    await session.commit()


async def remove_user_from_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    statement = select(Account).where(
        and_(Account.user_id == user_id, Account.group_id == group_id)
    )
    result = await session.execute(statement)
    account = result.scalar_one_or_none()

    if account:
        await session.delete(account)
        await session.commit()
