from fastapi import Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.celery.email_tasks import send_confirmation_email
from features.groups.services.group import get_user_groups
from features.groups.validators import get_group_or_404, get_account_or_404
from features.users.schemas import (
    EmailUpdate,
    EmailUpdateRead,
    UserProfileUpdate,
    UserProfileRead,
    UserProfileUpdatePartial,
)
from features.users.crud.user import get_user_by_id
from features.groups.services.account import leave_from_group
from features.users.validators import check_user_exists
from utils.JWT import create_email_confirmation_token

from features.users.crud.user_profile import (
    get_user_profile_by_id,
    update_profile,
)


async def delete_user(
    session: AsyncSession,
    user_id: int,
    request: Request,
    response: Response | None = None,
) -> None:

    user = await get_user_by_id(session=session, user_id=user_id)

    groups = await get_user_groups(session=session, user_id=user_id)

    for group in groups:
        await leave_from_group(session=session, user_id=user_id, group_id=group.id)

    await session.delete(user)

    if response is not None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        if "authorization" in request.headers:
            response.headers["Authorization"] = ""

    await session.commit()


async def update_user_profile(
    session: AsyncSession,
    user_data: UserProfileUpdate | UserProfileUpdatePartial,
    user_id: int,
    partial: bool = False,
) -> UserProfileRead:
    await check_user_exists(session, user_id)

    profile = await get_user_profile_by_id(session=session, profile_id=user_id)

    update_data = user_data.model_dump(exclude_unset=partial)

    updated_profile = await update_profile(
        session, profile=profile, update_data=update_data
    )

    return UserProfileRead.model_validate(updated_profile)


async def update_user_email(
    session: AsyncSession,
    user_data: EmailUpdate,
    user_id: int,
    request: Request,
    response: Response | None = None,
) -> EmailUpdateRead:
    await check_user_exists(session=session, user_id=user_id)

    user = await get_user_by_id(session=session, user_id=user_id)
    user.email = user_data.email

    user.is_verified = False
    token = create_email_confirmation_token(
        user_id=user.id,
        user_email=user_data.email,
    )

    await send_confirmation_email(
        request=request,
        email=user_data.email,
        token=token,
        html_file="verified_email",
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    if "authorization" in request.headers:
        response.headers["Authorization"] = ""

    await session.commit()
    await session.refresh(user)

    return EmailUpdateRead.model_validate(user)


async def get_int_role_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> int:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_or_404(session=session, group_id=group_id)
    account = await get_account_or_404(
        session=session, user_id=user_id, group_id=group_id
    )

    return account.role
