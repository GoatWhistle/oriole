from fastapi import HTTPException, Response, Request
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from features.groups.models import Account
from features.groups.schemas import AccountRole
from features.groups.services.group import get_user_groups
from features.groups.validators import get_group_if_exists, check_user_in_group
from features.users.models import User
from features.users.schemas import (
    EmailUpdate,
    EmailUpdateRead,
    UserProfileUpdate,
    UserProfileRead,
    UserProfileUpdatePartial,
)
from core.celery.email_tasks import send_confirmation_email
from features.users.validators import check_user_exists
from utils.JWT import create_email_confirmation_token


async def delete_user(
    session: AsyncSession,
    user_id: int,
    request: Request,
    response: Response | None = None,
) -> None:
    await check_user_exists(session=session, user_id=user_id)

    user = await session.get(User, user_id)

    groups = await get_user_groups(session=session, user_id=user_id)

    for group in groups:
        account = await session.execute(
            select(Account).where(
                Account.user_id == user_id, Account.group_id == group.id
            )
        )
        account = account.scalars().first()

        if account.role == AccountRole.OWNER.value:
            admins = await session.execute(
                select(Account).where(
                    Account.group_id == group.id,
                    Account.role == AccountRole.ADMIN.value,
                )
            )
            admin_accounts = admins.scalars().all()

            if admin_accounts:
                new_owner = min(admin_accounts, key=lambda a: a.user_id)
                new_owner.role = AccountRole.OWNER.value
            else:
                members = await session.execute(
                    select(Account).where(
                        Account.group_id == group.id,
                        Account.role == AccountRole.MEMBER.value,
                    )
                )
                member_accounts = members.scalars().all()

                if member_accounts:
                    new_owner = min(member_accounts, key=lambda a: a.user_id)
                    new_owner.role = AccountRole.OWNER.value

        await session.delete(account)

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
    await check_user_exists(session=session, user_id=user_id)

    user = await session.get(User, user_id, options=[joinedload(User.profile)])

    if not user.profile:
        raise HTTPException(
            status_code=400,
            detail="User profile not exists",
        )

    update_data = user_data.model_dump(exclude_unset=partial)
    for field in {"name", "surname", "patronymic"}:
        if field in update_data:
            setattr(user.profile, field, update_data[field])

    await session.commit()
    await session.refresh(user)

    return UserProfileRead.model_validate(user.profile)


async def update_user_email(
    session: AsyncSession,
    user_data: EmailUpdate,
    user_id: int,
    request: Request,
    response: Response | None = None,
) -> EmailUpdateRead:
    await check_user_exists(session=session, user_id=user_id)

    user = await session.get(User, user_id)
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
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, user_id=user_id, group_id=group_id)

    statement_account = select(Account).where(Account.user_id == user_id)
    result_account: Result = await session.execute(statement_account)
    account = result_account.scalars().first()

    return account.role
