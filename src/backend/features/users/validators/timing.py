from datetime import datetime

from cryptography.hazmat.backends.openssl import backend
from pytz import utc

from fastapi import (
    HTTPException,
    status,
    Response,
    Request,
)
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession


from utils.JWT import (
    decode_jwt,
)
from features.users.services.operations import refresh_tokens_operation


def get_current_token_payload(
    token: str,
) -> dict:
    try:
        return backend.utils.JWT.get_current_token_payload(token=token)

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )


def check_expiration_after_redirect(payload: dict):
    current_time_utc = datetime.now(utc).timestamp()
    if not (int(current_time_utc) < int(payload.get("exp", 0))):
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="The request time has expired",
        )


def validate_token_expiration(token: str) -> bool:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        current_time_utc = datetime.now(utc).timestamp()
        return int(current_time_utc) >= int(payload.get("exp", 0))

    except Exception as ex:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        ) from ex


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
        raise HTTPException(status_code=401, detail="Token is missing")

    new_token = await refresh_if_needed(
        request=request,
        response=response,
        session=session,
        token=token,
    )
    return new_token if new_token else token
