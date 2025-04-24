from fastapi import HTTPException, status

from typing import Sequence
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession


from core.exceptions.group import (
    check_group_exists,
    check_admin_permission_in_group,
    check_user_in_group,
)
from core.exceptions.user import check_user_exists
from core.schemas.user import (
    UserRead,
    UserUpdate,
    UserUpdatePartial,
)
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead
from core.schemas.assignment import AssignmentRead
from core.schemas.account import AccountRole


from core.models import User, Group, Account, Assignment, Task


async def delete_user(
    session: AsyncSession,
    current_user_id: int,
    deleted_user_id: int,
) -> None:
    await check_user_exists(session=session, user_id=deleted_user_id)

    if not deleted_user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owner can delete his account",
        )

    deleted_user = await session.get(User, deleted_user_id)

    async with session.begin_nested():
        accounts = await session.execute(
            select(Account).where(Account.user_id == deleted_user)
        )
        for account in accounts.scalars():
            await session.delete(account)

        await session.delete(deleted_user.profile)

        assignments = await session.execute(
            select(Assignment).where(Assignment.admin_id == deleted_user_id)
        )
        for assignment in assignments.scalars():
            await session.delete(assignment)

        await session.delete(deleted_user)

    await session.commit()


# TODO: в случае если апдейт по почте ебанной, то поставить is_verified = False
async def update_user(
    session: AsyncSession,
    user_id: int,
    user_data: UserUpdate | UserUpdatePartial,
    current_user_id: int,
    partial: bool = False,
) -> UserRead:
    await check_user_exists(session=session, user_id=user_id)

    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    user = await session.get(User, user_id)

    user_to_go = {}
    profile_to_go = {}

    for key, value in user_data.model_dump(exclude_unset=partial).items():
        if key == "email":
            user_to_go[key] = value
        elif key in {"name", "surname", "patronymic"}:
            profile_to_go[key] = value

    if profile_to_go:
        for key, value in profile_to_go.items():
            setattr(user.profile, key, value)
        session.add(user.profile)
        await session.flush()

    if user_to_go:
        for key, value in user_to_go.items():
            setattr(user, key, value)
        session.add(user)
        await session.flush()

    await session.commit()
    await session.refresh(user)

    return UserRead.model_validate(user)
