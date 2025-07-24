from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.accounts.mappers as mapper
import features.groups.crud.group_invite as group_invite_crud
import features.spaces.crud.space_join_request as space_join_request_crud
import features.spaces.mappers as space_mapper
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
    get_group_invite_by_code_or_404,
    is_account_exists,
)
from features.spaces.schemas import SpaceJoinStatusRead, SpaceJoinRequestCreate
from features.spaces.validators import (
    get_space_or_404,
    check_space_invite_active,
    is_space_join_requests_exists,
)
from features.users.validators import check_user_exists
from shared.enums.space_join_request import SpaceJoinStatusEnum


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


async def join_to_group(
    session: AsyncSession,
    user_id: int,
    group_invite_code: str,
) -> SpaceJoinStatusRead:
    group_invite = await get_group_invite_by_code_or_404(session, group_invite_code)
    check_space_invite_active(group_invite.is_active)

    if await is_account_exists(session, user_id, group_invite.space_id):
        return space_mapper.build_space_join_status_read(
            SpaceJoinStatusEnum.ALREADY_JOINED, user_id, group_invite.space_id
        )

    if await is_space_join_requests_exists(session, user_id, group_invite.space_id):
        return space_mapper.build_space_join_status_read(
            SpaceJoinStatusEnum.ALREADY_REQUESTED, user_id, group_invite.space_id
        )

    await group_invite_crud.increment_group_invite_user_usages_count(
        session, group_invite
    )

    if group_invite.needs_approval:
        space_join_request_create = SpaceJoinRequestCreate(
            user_id=user_id,
            space_id=group_invite.space_id,
            space_invite_id=group_invite.id,
        )
        await space_join_request_crud.create_space_join_request(
            session, space_join_request_create
        )
        return space_mapper.build_space_join_status_read(
            SpaceJoinStatusEnum.REQUESTED, user_id, group_invite.space_id
        )
    else:
        await account_crud.create_account(
            session, user_id, group_invite.space_id, AccountRole.MEMBER.value
        )

        return space_mapper.build_space_join_status_read(
            SpaceJoinStatusEnum.JOINED, user_id, group_invite.space_id
        )
