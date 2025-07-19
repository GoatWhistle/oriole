from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.group_invite as group_invite_crud
import features.groups.mappers as mapper
from features.groups.schemas import (
    GroupInviteCreate,
    GroupInviteUpdate,
    GroupInviteReadWithLink,
)
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
    get_group_invite_by_id_or_404,
)


async def create_group_invite(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_invite_create: GroupInviteCreate,
) -> GroupInviteReadWithLink:
    _ = await get_group_or_404(session, group_invite_create.space_id)
    account = await get_account_or_404(session, user_id, group_invite_create.space_id)

    check_user_is_admin_or_owner(account.role)

    group_invite = await group_invite_crud.create_group_invite(
        session, group_invite_create, account.id
    )
    return mapper.build_group_invite_read_with_link(group_invite, request)


async def get_group_invite_by_id(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_invite_id: int,
) -> GroupInviteReadWithLink:
    group_invite = await get_group_invite_by_id_or_404(session, group_invite_id)
    _ = await get_group_or_404(session, group_invite.space_id)
    account = await get_account_or_404(session, user_id, group_invite.space_id)

    check_user_is_admin_or_owner(account.role)

    return mapper.build_group_invite_read_with_link(group_invite, request)


async def get_group_invites_in_group(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_id: int,
    is_active: bool | None = None,
) -> list[GroupInviteReadWithLink]:
    _ = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    check_user_is_admin_or_owner(account.role)

    group_invites = await group_invite_crud.get_group_invites_by_group_id(
        session, group_id, is_active
    )

    return mapper.build_group_invite_read_with_link_list(group_invites, request)


async def update_group_invite(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_invite_id: int,
    group_invite_update: GroupInviteUpdate,
) -> GroupInviteReadWithLink:
    group_invite = await get_group_invite_by_id_or_404(session, group_invite_id)
    _ = await get_group_or_404(session, group_invite.space_id)
    account = await get_account_or_404(session, user_id, group_invite.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = group_invite_update.model_dump(exclude_unset=True)
    group_invite = await group_invite_crud.update_group_invite(
        session, group_invite, update_data
    )

    return mapper.build_group_invite_read_with_link(group_invite, request)


async def delete_group_invite(
    session: AsyncSession,
    user_id: int,
    group_invite_id: int,
) -> None:
    group_invite = await get_group_invite_by_id_or_404(session, group_invite_id)
    _ = await get_group_or_404(session, group_invite.space_id)
    account = await get_account_or_404(session, user_id, group_invite.space_id)

    check_user_is_admin_or_owner(account.role)

    await group_invite_crud.delete_group_invite(session, group_invite)


async def delete_group_invites_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    is_active: bool | None = None,
) -> None:
    _ = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    check_user_is_admin_or_owner(account.role)

    await group_invite_crud.delete_group_invites_by_group_id(
        session, group_id, is_active
    )
