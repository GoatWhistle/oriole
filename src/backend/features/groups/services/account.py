from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import Account
from features.groups.schemas.account import AccountRole
from features.groups.validators import (
    get_group_if_exists,
    check_admin_permission_in_group,
    check_owner_permission_in_group,
    check_user_in_group,
    check_user_is_member,
)
from features.tasks.models import UserReply
from features.users.validators import check_user_exists


async def promote_user_to_admin(
    session: AsyncSession,
    user_id: int,
    promote_user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=promote_user_id)

    _ = await get_group_if_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=promote_user_id
    )

    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(
        Account.user_id == promote_user_id, Account.group_id == group_id
    )
    result: Result = await session.execute(statement)
    account = result.scalars().first()

    await check_user_is_member(role=account.role, user_id=user_id)

    account.role = AccountRole.ADMIN

    await session.commit()


async def demote_user_to_member(
    session: AsyncSession,
    user_id: int,
    demote_user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=demote_user_id)

    _ = await get_group_if_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=demote_user_id
    )

    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(
        Account.user_id == demote_user_id, Account.group_id == group_id
    )
    result: Result = await session.execute(statement)
    account = result.scalars().first()

    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    account.role = AccountRole.MEMBER

    await session.commit()


async def remove_user_from_group(
    session: AsyncSession,
    user_id: int,
    remove_user_id: int,
    group_id: int,
) -> None:
    if user_id == remove_user_id:
        await leave_from_group(session=session, user_id=user_id, group_id=group_id)
        return

    await check_user_exists(session=session, user_id=user_id)
    await check_user_exists(session=session, user_id=remove_user_id)

    _ = await get_group_if_exists(session=session, group_id=group_id)

    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_user_in_group(
        session=session, group_id=group_id, user_id=remove_user_id
    )

    await check_owner_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    statement = select(Account).where(
        Account.user_id == remove_user_id, Account.group_id == group_id
    )
    result: Result = await session.execute(statement)
    account = result.scalars().first()

    await session.execute(delete(UserReply).where(UserReply.account_id == account.id))

    await session.delete(account)
    await session.commit()


async def leave_from_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    account = await session.execute(
        select(Account).where(Account.user_id == user_id, Account.group_id == group_id)
    )
    account = account.scalars().first()

    await session.execute(delete(UserReply).where(UserReply.account_id == account.id))
    if account.role == AccountRole.OWNER.value:
        admins = await session.execute(
            select(Account).where(
                Account.group_id == group_id, Account.role == AccountRole.ADMIN.value
            )
        )
        admin_accounts = admins.scalars().all()

        if admin_accounts:
            new_owner = min(admin_accounts, key=lambda a: a.user_id)
            new_owner.role = AccountRole.OWNER.value
            account.role = AccountRole.MEMBER.value
        else:
            members = await session.execute(
                select(Account).where(
                    Account.group_id == group_id,
                    Account.role == AccountRole.MEMBER.value,
                )
            )
            member_accounts = members.scalars().all()

            if member_accounts:
                new_owner = min(member_accounts, key=lambda a: a.user_id)
                new_owner.role = AccountRole.OWNER.value
                account.role = AccountRole.MEMBER.value

    await session.delete(account)
    await session.commit()
