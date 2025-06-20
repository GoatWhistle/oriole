from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.account as account_crud
from features.groups.schemas import AccountRole
from features.groups.validators import (
    get_group_if_exists,
    get_account_if_exists,
    check_user_is_member,
    check_user_is_owner,
    check_user_is_admin,
)
from features.users.validators import check_user_exists


async def promote_user_to_admin(
    session: AsyncSession,
    user_id: int,
    promote_user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session, user_id)
    await check_user_exists(session, promote_user_id)

    _ = await get_group_if_exists(session, group_id)

    account = await get_account_if_exists(session, group_id, user_id)
    promote_account = await get_account_if_exists(session, group_id, promote_user_id)

    check_user_is_owner(account.role, user_id)
    check_user_is_member(promote_account.role, user_id)

    await account_crud.update_account_role(
        session, promote_account, AccountRole.ADMIN.value
    )


async def demote_user_to_member(
    session: AsyncSession,
    user_id: int,
    demote_user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session, user_id)
    await check_user_exists(session, demote_user_id)

    _ = await get_group_if_exists(session, group_id)

    account = await get_account_if_exists(session, group_id, user_id)
    demote_account = await get_account_if_exists(session, group_id, demote_user_id)

    check_user_is_owner(account.role, user_id)
    check_user_is_admin(demote_account.role, demote_user_id)

    await account_crud.update_account_role(
        session, demote_account, AccountRole.MEMBER.value
    )


async def remove_user_from_group(
    session: AsyncSession,
    user_id: int,
    remove_user_id: int,
    group_id: int,
) -> None:
    if user_id == remove_user_id:
        await leave_from_group(session, user_id, group_id)
        return

    await check_user_exists(session, user_id)
    await check_user_exists(session, remove_user_id)

    _ = await get_group_if_exists(session, group_id)

    account = await get_account_if_exists(session, group_id, user_id)
    remove_account = await get_account_if_exists(session, group_id, remove_user_id)

    check_user_is_owner(account.role, user_id)

    await account_crud.delete_user_replies_by_account_id(session, remove_account.id)
    await account_crud.delete_account(session, remove_account)


async def leave_from_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session, user_id)

    _ = await get_group_if_exists(session, group_id)
    account = await get_account_if_exists(session, user_id, group_id)

    await account_crud.delete_user_replies_by_account_id(session, account.id)

    if account.role == AccountRole.OWNER:
        admins = await account_crud.get_admins_accounts_by_group(session, group_id)

        if admins:
            new_owner = min(admins, key=lambda a: a.user_id)
            new_owner.role = AccountRole.OWNER
        else:
            members = await account_crud.get_members_accounts_by_group(
                session, group_id
            )
            if members:
                new_owner = min(members, key=lambda a: a.user_id)
                new_owner.role = AccountRole.OWNER

    await account_crud.delete_account(session, account)
