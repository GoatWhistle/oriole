from fastapi import HTTPException, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from crud.email_access import send_confirmation_email
from exceptions.user import check_user_exists
from core.schemas.user import (
    EmailUpdate,
    EmailUpdateRead,
    UserProfileUpdate,
    UserProfileRead,
    UserProfileUpdatePartial,
)
from core.models import User
from utils.JWT import create_email_confirmation_token


async def delete_user(
    session: AsyncSession,
    user_id: int,
    request: Request,
    response: Response | None = None,
) -> None:
    await check_user_exists(session=session, user_id=user_id)

    user = await session.get(User, user_id)

    await session.delete(user)

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
        email=user_data.email,
        token=token,
        html_file="verified_email",
        address_type="email_verify",
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    if "authorization" in request.headers:
        response.headers["Authorization"] = ""

    await session.commit()
    await session.refresh(user)

    return EmailUpdateRead.model_validate(user)
