from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from groups.models import Account
from groups.schemas import AccountRole


async def check_user_in_group(
    session: AsyncSession,
    user_id: int | Mapped[int],
    group_id: int | Mapped[int],
    is_correct: bool = True,
) -> None:
    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    if not account and is_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} is not a member of group {group_id}.",
        )
    elif account and not is_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_id} is already a member of group {group_id}.",
        )


async def check_user_is_member(
    role: int | Mapped[int],
    user_id: int | Mapped[int],
) -> None:
    if role != AccountRole.MEMBER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_id} having not a MEMBER role cannot be promoted.",
        )
