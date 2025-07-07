from fastapi import Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from core.celery.email_tasks import send_confirmation_email
from features.accounts.services.account import leave_from_space
from features.groups.services.group import get_user_groups
from features.groups.validators import get_group_or_404, get_account_or_404
from features.users.schemas import (
    UserProfileUpdate,
    UserProfileRead,
    UserProfileUpdatePartial,
)
from features.groups.services.account import leave_from_group
from utils.JWT import create_email_update_token

from features.users.validators.existence import (
    has_any_token,
    ensure_user_exists,
    ensure_user_exists_by_email,
)
from features.users.services.token_operations import clear_auth_tokens

from features.users.crud.user_profile import (
    update_profile,
    get_user_profile_by_user_id,
)


async def delete_user(
    session: AsyncSession,
    user_id: int,
    request: Request,
    response: Response | None = None,
) -> None:
    user = await ensure_user_exists(session=session, user_id=user_id)

    groups = await get_user_groups(session=session, user_id=user_id)

    for group in groups:
        await leave_from_space(session=session, user_id=user_id, group_id=group.id)

    await session.delete(user)

    if response and has_any_token(request):
        clear_auth_tokens(request, response)

    await session.commit()


async def change_user_email(
    request: Request,
    email: EmailStr,
    new_email: EmailStr,
    session: AsyncSession,
) -> dict:
    user = await ensure_user_exists_by_email(session=session, email=email)

    token = create_email_update_token(
        user_id=user.id,
        old_email=user.email,
        new_email=new_email,
    )

    await send_confirmation_email(
        request=request,
        email=new_email,
        token=token,
        html_file="email_update_warning.html",
        address_type="change_email",
    )

    return {"message": "Email change link has been sent to your new email"}


async def update_user_profile(
    session: AsyncSession,
    user_data: UserProfileUpdate | UserProfileUpdatePartial,
    user_id: int,
    partial: bool = False,
) -> UserProfileRead:
    await ensure_user_exists(session, user_id)

    profile = await get_user_profile_by_user_id(session=session, user_id=user_id)

    update_data = user_data.model_dump(exclude_unset=partial)

    updated_profile = await update_profile(
        session,
        profile=profile,
        update_data=update_data,
    )

    return UserProfileRead.model_validate(updated_profile)


async def get_int_role_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> int:
    await ensure_user_exists(session=session, user_id=user_id)
    await get_group_or_404(session=session, group_id=group_id)
    account = await get_account_or_404(
        session=session,
        user_id=user_id,
        space_id=group_id,
    )

    return account.role
