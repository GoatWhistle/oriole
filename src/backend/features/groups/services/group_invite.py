from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.group_invite as group_invite_crud
from features.groups.schemas import (
    GroupInviteRead,
    GroupInviteCreate,
    GroupInviteUpdate,
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
) -> GroupInviteRead:
    _ = await get_group_or_404(session, group_invite_create.space_id)
    account = await get_account_or_404(session, user_id, group_invite_create.space_id)

    check_user_is_admin_or_owner(account.role)

    group_invite = await group_invite_crud.create_group_invite(
        session, group_invite_create, account.id
    )
    base_url = str(request.base_url).rstrip("/")
    return group_invite.get_validation_schema(base_url=base_url)


async def get_group_invite_by_id(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_invite_id: int,
) -> GroupInviteRead:
    group_invite = await get_group_invite_by_id_or_404(session, group_invite_id)
    _ = await get_group_or_404(session, group_invite.space_id)
    account = await get_account_or_404(session, user_id, group_invite.space_id)

    check_user_is_admin_or_owner(account.role)

    base_url = str(request.base_url).rstrip("/")
    return group_invite.get_validation_schema(base_url=base_url)


async def get_group_invites_in_group(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_id: int,
    is_active: bool | None = None,
) -> list[GroupInviteRead]:
    _ = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    check_user_is_admin_or_owner(account.role)

    invites = await group_invite_crud.get_group_invites_by_group_id(
        session, group_id, is_active
    )

    base_url = str(request.base_url).rstrip("/")
    return [invite.get_validation_schema(base_url=base_url) for invite in invites]


async def update_group_invite(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_invite_id: int,
    group_invite_update: GroupInviteUpdate,
) -> GroupInviteRead:
    group_invite = await get_group_invite_by_id_or_404(session, group_invite_id)
    _ = await get_group_or_404(session, group_invite.space_id)
    account = await get_account_or_404(session, user_id, group_invite.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = group_invite_update.model_dump(exclude_unset=True)
    group_invite = await group_invite_crud.update_group_invite(
        session, group_invite, update_data
    )

    base_url = str(request.base_url).rstrip("/")
    return group_invite.get_validation_schema(base_url=base_url)


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
