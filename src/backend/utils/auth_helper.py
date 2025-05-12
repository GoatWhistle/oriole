from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    HTTPException,
    status,
    Depends,
    Response,
    Request,
)
from crud.auth import OAuth2_scheme, refresh_tokens
from sqlalchemy.orm import Mapped

from utils.JWT import decode_jwt
from jwt.exceptions import InvalidTokenError
from exceptions.user import validate_activity_and_verification

from core.models import User, db_helper
from core.schemas.user import (
    UserAuth,
    UserAuthRead,
)
from datetime import datetime
from pytz import utc


async def refresh_if_needed(
    request: Request,
    response: Response,
    session: AsyncSession,
    token: str | None,
) -> str | None:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        current_time_utc = datetime.now(utc).timestamp()
        if int(current_time_utc) < int(payload.get("exp", 0)):
            return None

        return await refresh_tokens(
            request=request,
            response=response,
            session=session,
        )
    except HTTPException:
        return None


def get_current_token_payload(
    token: str,
) -> dict:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        return payload

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )


async def get_non_expire_payload_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    token: str | None = Depends(OAuth2_scheme),
) -> str:
    if token:
        new_token = await refresh_if_needed(
            request=request,
            response=response,
            session=session,
            token=token,
        )
        if new_token:
            token = new_token
        return get_current_token_payload(token)

    # значит что токенов нет: есть только рефреш
    new_token = await refresh_tokens(request, response, session)
    return get_current_token_payload(new_token)


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    payload: dict = Depends(get_non_expire_payload_token),
) -> UserAuth:
    email = payload.get("email")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (email not found in payload)",
        )

    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    await validate_activity_and_verification(user_from_db=user_from_db)

    return UserAuthRead.model_validate(user_from_db)


def get_current_active_auth_user_id(
    user_from_db: UserAuthRead = Depends(get_current_auth_user),
) -> int | Mapped[int]:
    return user_from_db.id
