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
) -> None:
    user = await user_crud.get_user_by_id(session, user_id)
    if not user:
        raise UserNotFoundException()


async def ensure_user_exists(
    session: AsyncSession,
    user_id: int,
) -> User:
    user = await user_crud.get_user_by_id(session, user_id)
    if not user:
        raise UserNotFoundException()
    return user


async def ensure_user_exists_by_email(
    session: AsyncSession,
    email: EmailStr,
) -> User:
    user = await user_crud.get_user_by_email(session, email)
    if not user:
        raise UserNotFoundException()
    return user


async def ensure_user_not_exists_by_email(
    session: AsyncSession,
    email: EmailStr,
) -> None:
    if await user_crud.get_user_by_email(session, email):
        raise UserAlreadyRegisteredException()


async def get_user_if_exists(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await user_crud.get_user_by_id(session, user_id)


async def get_user_by_email_if_exists(
    session: AsyncSession,
    email: EmailStr,
) -> User | None:
    return await user_crud.get_user_by_email(session, email)


async def check_email_available(
    session: AsyncSession,
    email: EmailStr,
) -> bool:
    return not await user_crud.get_user_by_email(session, email)


async def get_user_profile_if_exists(
    session: AsyncSession,
    user_id: int,
) -> UserProfile:
    profile = await user_profile_crud.get_user_profile_by_user_id(session, user_id)
    if not profile:
        raise ProfileNotFoundException()
    return profile


async def ensure_user_profile_exists(
    session: AsyncSession, email: EmailStr
) -> UserProfile:
    profile = await user_profile_crud.get_user_profile_by_email(session, email)
    if not profile:
        raise ProfileNotFoundException()
    return profile


async def check_user_profile_exists(
    session: AsyncSession, email: EmailStr
) -> UserProfile | None:
    return await user_profile_crud.get_user_profile_by_email(session, email)


def ensure_no_tokens(request: Request) -> None:
    if has_any_token(request):
        raise AuthenticatedForbiddenException()


def ensure_has_tokens(request: Request) -> None:
    if not has_any_token(request):
        raise AuthenticationRequiredException()


def has_any_token(request: Request) -> bool:
    return (
        any(token in request.cookies for token in ("access_token", "refresh_token"))
        or "authorization" in request.headers
    )


def get_token_presence(request: Request) -> tuple[bool, bool]:
    return (
        any(token in request.cookies for token in ("access_token", "refresh_token")),
        "authorization" in request.headers,
    )


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
