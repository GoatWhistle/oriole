from fastapi import Request
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

import features.users.crud.user as user_crud
import features.users.crud.user_profile as user_profile_crud
from features import User, UserProfile
from features.users.exceptions import (
    UserNotFoundException,
    UserAlreadyRegisteredException,
    ProfileNotFoundException,
)
from features.users.exceptions import (
    AuthenticationRequiredException,
    AuthenticatedForbiddenException,
    EmailRequiredExceptions,
)
from shared.exceptions.token import InvalidTokenException


async def check_user_exists(
    session: AsyncSession,
    user_id: int,
    raise_exception: bool = True,
) -> User:
    user = await user_crud.get_user_by_id(session, user_id)
    if not user and raise_exception:
        raise UserNotFoundException()
    return user


async def check_user_exists_using_email(
    session: AsyncSession,
    email: EmailStr,
    raise_exception: bool = True,
) -> User:
    user = await user_crud.get_user_by_email(session=session, email=email)
    if not user and raise_exception:
        raise UserNotFoundException()
    return user


async def check_user_not_exists_using_email(
    session: AsyncSession,
    email: EmailStr,
    raise_exception: bool = True,
) -> bool:
    user = await user_crud.get_user_by_email(session=session, email=email)
    if user and raise_exception:
        raise UserAlreadyRegisteredException()
    return not user


async def get_user_profile_if_exists(
    session: AsyncSession,
    user_id: int,
) -> UserProfile:
    profile = await user_profile_crud.get_user_profile_by_user_id(session, user_id)
    if not profile:
        raise ProfileNotFoundException()
    return profile


async def validate_user_profile_exists(
    session: AsyncSession,
    email: EmailStr,
    raise_exception: bool = True,
) -> UserProfile:
    profile = await user_profile_crud.get_user_profile_by_email(
        session=session,
        email=email,
    )
    if not profile and raise_exception:
        raise ProfileNotFoundException()
    return profile


def validate_token_presence(
    request: Request,
    mode: str = "require",
    raise_exception: bool = True,
) -> None | tuple:
    has_cookie = any(
        token in request.cookies for token in ("access_token", "refresh_token")
    )
    has_header = "authorization" in request.headers

    if mode == "forbid" and (has_cookie or has_header):
        if raise_exception:
            raise AuthenticatedForbiddenException()
        return has_cookie, has_header

    if mode == "require" and not (has_cookie or has_header):
        if raise_exception:
            raise AuthenticationRequiredException()
        return has_cookie, has_header

    return None if raise_exception else (has_cookie, has_header)


def validate_token_has_email(payload: dict) -> str:
    if not (email := payload.get("email")):
        raise InvalidTokenException("email not found in payload")
    return email


def validate_token_has_user_id(payload: dict) -> int:
    try:
        return int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise InvalidTokenException("invalid user ID")


def is_email_entered(email: str):
    if not email:
        raise EmailRequiredExceptions()
    return email
