from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from groups.models import Account
from groups.schemas import AccountRole


async def check_admin_permission_in_group(
    session: AsyncSession,
    user_id: int | Mapped[int],
    group_id: int | Mapped[int],
) -> None:
    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    if account.role not in (AccountRole.OWNER.value, AccountRole.ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have ADMIN permission to perform this action in group {group_id}.",
        )


async def check_owner_permission_in_group(
    session: AsyncSession,
    user_id: int | Mapped[int],
    group_id: int | Mapped[int],
) -> None:
    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    if account.role != AccountRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have OWNER permission to perform this action in group {group_id}.",
        )
