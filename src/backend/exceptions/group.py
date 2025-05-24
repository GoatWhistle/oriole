from fastapi import HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.models import Account, Group
from core.models.group_invite import GroupInvite
from core.schemas.account import AccountRole
from utils.time_manager import get_current_utc_timestamp


async def get_group_if_exists(
    session: AsyncSession,
    group_id: Mapped[int] | int,
) -> Group:
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} not found",
        )
    return group


async def check_user_in_group(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    group_id: Mapped[int] | int,
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


async def check_admin_permission_in_group(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    group_id: Mapped[int] | int,
) -> None:

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    if account.role not in (AccountRole.OWNER.value, AccountRole.ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have admin permission to perform this action in group {group_id}.",
        )


async def check_owner_permission_in_group(
    session: AsyncSession,
    user_id: Mapped[int] | int,
    group_id: Mapped[int] | int,
) -> None:

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()  #

    if account.role != AccountRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have owner permission to perform this action in group {group_id}.",
        )


async def check_user_is_member(
    role: Mapped[int] | int,
    user_id: Mapped[int] | int,
):
    if role != AccountRole.MEMBER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_id} is not a MEMBER and cannot be promoted.",
        )


async def check_invite_exists(
    session: AsyncSession,
    code: str,
) -> GroupInvite:
    result = await session.execute(
        select(GroupInvite).where(GroupInvite.code == code)
    )
    invite = result.scalars().first()

    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invite code does not exist"
        )
    return invite


async def check_invite_active(
    invite: GroupInvite,
) -> None:

    if not invite.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invite code is no longer active"
        )


async def check_invite_not_expired(
    invite: GroupInvite,
) -> None:
    if invite.expires_at < get_current_utc_timestamp() :
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invite code has expired"
        )


async def validate_invite_code(
    session: AsyncSession,
    code: str,
) -> GroupInvite:
    invite = await session.execute(
        select(GroupInvite)
        .where(GroupInvite.code == code)
    )
    invite = invite.scalars().first()

    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invite code"
        )

    if not invite.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invite is no longer active"
        )

    if invite.expires_at < get_current_utc_timestamp() :
        invite.is_active = False
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invite has expired"
        )

    return invite