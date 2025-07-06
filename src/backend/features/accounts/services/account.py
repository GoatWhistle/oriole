from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.accounts.mappers as mapper
import features.users.crud.user_profile as user_profile_crud
from features.accounts.schemas import (
    AccountRole,
    AccountRead,
    AccountReadWithProfileData,
)
from features.groups.validators import (
    get_account_or_404,
    check_user_is_member,
    check_user_is_owner,
    check_user_is_admin,
)
from features.spaces.validators import get_space_or_404
from features.users.validators import check_user_exists


async def get_accounts_in_space(
    session: AsyncSession,
    user_id: int,
    space_id: int,
) -> list[AccountReadWithProfileData]:
    _ = await get_space_or_404(session, space_id)
    _ = await get_account_or_404(session, user_id, space_id)

    accounts = await account_crud.get_accounts_by_space_id(session, space_id)
    user_profiles = await user_profile_crud.get_user_profiles_by_user_ids(
        session, [account.user_id for account in accounts]
    )
    return mapper.build_account_read_with_profile_data_list(accounts, user_profiles)


async def promote_user_to_admin(
    session: AsyncSession,
    user_id: int,
    promote_user_id: int,
    space_id: int,
) -> AccountRead:
    await check_user_exists(session, promote_user_id)

    _ = await get_space_or_404(session, space_id)

    account = await get_account_or_404(session, space_id, user_id)
    promote_account = await get_account_or_404(session, space_id, promote_user_id)

    check_user_is_owner(account.role)
    check_user_is_member(promote_account.role)

    account = await account_crud.update_account_role(
        session, promote_account, AccountRole.ADMIN.value
    )
    return account.get_validation_schema()


async def demote_user_to_member(
    session: AsyncSession,
    user_id: int,
    demote_user_id: int,
    space_id: int,
) -> AccountRead:
    await check_user_exists(session, demote_user_id)

    _ = await get_space_or_404(session, space_id)

    account = await get_account_or_404(session, space_id, user_id)
    demote_account = await get_account_or_404(session, space_id, demote_user_id)

    check_user_is_owner(account.role)
    check_user_is_admin(demote_account.role)

    account = await account_crud.update_account_role(
        session, demote_account, AccountRole.MEMBER.value
    )
    return account.get_validation_schema()


async def remove_user_from_space(
    session: AsyncSession,
    user_id: int,
    remove_user_id: int,
    space_id: int,
) -> None:
    if user_id == remove_user_id:
        await leave_from_space(session, user_id, space_id)
        return

    await check_user_exists(session, remove_user_id)

    _ = await get_space_or_404(session, space_id)

    account = await get_account_or_404(session, space_id, user_id)
    remove_account = await get_account_or_404(session, space_id, remove_user_id)

    check_user_is_owner(account.role)

    await account_crud.delete_solutions_by_account_id(session, remove_account.id)
    await account_crud.delete_account(session, remove_account)


async def leave_from_space(
    session: AsyncSession,
    user_id: int,
    space_id: int,
) -> None:
    _ = await get_space_or_404(session, space_id)
    account = await get_account_or_404(session, user_id, space_id)

    await account_crud.delete_solutions_by_account_id(session, account.id)

    if account.role == AccountRole.OWNER:
        admins = await account_crud.get_accounts_by_space_and_role(
            session, space_id, AccountRole.ADMIN
        )

        if admins:
            new_owner = min(admins, key=lambda a: a.user_id)
            new_owner.role = AccountRole.OWNER
        else:
            members = await account_crud.get_accounts_by_space_and_role(
                session, space_id, AccountRole.MEMBER
            )
            if members:
                new_owner = min(members, key=lambda a: a.user_id)
                new_owner.role = AccountRole.OWNER

    await account_crud.delete_account(session, account)
