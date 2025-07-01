from datetime import datetime

from fastapi import Response, Request
from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import (
    RequestTimeoutException,
    InvalidTokenException,
    MissingTokenException,
)
from features.users.services.token_operations import refresh_tokens_operation
from utils.JWT import decode_jwt


def check_expiration_after_redirect(payload: dict):
    current_time_utc = datetime.now(utc).timestamp()
    if not (int(current_time_utc) < int(payload.get("exp", 0))):
        raise RequestTimeoutException()


def validate_token_expiration(token: str) -> bool:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        current_time_utc = datetime.now(utc).timestamp()
        return int(current_time_utc) >= int(payload.get("exp", 0))

    except Exception as ex:
        raise InvalidTokenException() from ex


async def refresh_if_needed(
    request: Request,
    response: Response,
    session: AsyncSession,
    token: str | None,
) -> str | None:
    if not token:
        return None

    is_expired = validate_token_expiration(token=token)
    if not is_expired:
        return None

    return await refresh_tokens_operation(
        request=request,
        response=response,
        session=session,
    )


async def validate_and_refresh_token(
    token: str,
    request: Request,
    response: Response,
    session: AsyncSession,
) -> str:
    if not token:
        raise MissingTokenException()

    new_token = await refresh_if_needed(
        request=request,
        response=response,
        session=session,
        token=token,
    )
    return new_token if new_token else token
