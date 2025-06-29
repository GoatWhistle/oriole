from fastapi import (
    HTTPException,
    status,
    Response,
    Request,
)
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings

from features.users.crud.user import (
    get_user_by_email,
)


from features.users.validators.timing import (
    get_current_token_payload,
    validate_and_refresh_token,
)
from features.users.validators.rules import validate_activity_and_verification

from utils.JWT import (
    create_access_token,
    create_refresh_token,
    decode_jwt,
)


def _set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    access_expires: int,
    refresh_expires: int,
) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=access_expires,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        path="/",
        max_age=refresh_expires,
    )


async def refresh_tokens_operation(
    request: Request,
    response: Response,
    session: AsyncSession,
) -> str:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing, sign in again",
        )

    try:
        payload = decode_jwt(refresh_token)
        user_email = payload.get("email")
        user_id = payload.get("sub")

        if not user_email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_from_db = await get_user_by_email(session=session, email=user_email)

        await validate_activity_and_verification(user_from_db=user_from_db)

        access_token = create_access_token(user_id, user_email)
        refresh_token = create_refresh_token(user_id, user_email)

        _set_auth_cookies(
            response=response,
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires=settings.auth_jwt.access_token_lifetime_seconds,
            refresh_expires=settings.auth_jwt.refresh_token_lifetime_seconds,
        )

        return f"Bearer {access_token}"

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


async def get_valid_payload(
    request: Request,
    response: Response,
    session: AsyncSession,
    token: str | None,
) -> dict:

    if token:
        valid_token = await validate_and_refresh_token(
            token=token,
            request=request,
            response=response,
            session=session,
        )
    else:
        valid_token = await refresh_tokens_operation(
            request=request,
            response=response,
            session=session,
        )

    return get_current_token_payload(valid_token)
