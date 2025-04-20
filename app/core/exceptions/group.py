from fastapi import HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.models import Account, Group
from core.schemas.account import AccountRole


async def check_group_exists(
    session: AsyncSession,
    group_id: Mapped[int] | int,
) -> None:
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} not found",
        )


async def check_user_in_group(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    group_id: Mapped[int] | int,
) -> None:

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} is not a member of group {group_id}.",
        )


async def check_admin_permission_in_group(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    group_id: Mapped[int] | int,
) -> None:
    group = await session.get(Group, group_id)
    account = next((acc for acc in group.accounts if acc.user_id == user_id), None)

    if not account or account.role != AccountRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have permission to perform this action in group {group_id}.",
        )
