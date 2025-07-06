from fastapi import Response


from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings

from utils.JWT import create_access_token, create_refresh_token
from features.users.schemas.token import TokenResponseForOAuth2
from features.users.services.token_operations import _set_auth_cookies
from features.users.schemas.telegram_user import TelegramUserData
from features.users import User
from features.users.crud.telegram_user import (
    get_user_by_telegram_id,
    create_user_via_telegram,
)

from features.users.validators.telegram import (
    ensure_hash_exists,
    validate_telegram_hash,
    validate_auth_date,
)


async def login_via_telegram(
    raw_data: dict,
    response: Response,
    session: AsyncSession,
):
    user = await authenticate_via_telegram(session, raw_data)

    access_token = create_access_token(
        user.id,
        user.email or f"tg:{user.telegram_id}",
        auth_method="telegram",
    )
    refresh_token = create_refresh_token(
        user.id,
        user.email or f"tg:{user.telegram_id}",
        auth_method="telegram",
    )

    _set_auth_cookies(
        response=response,
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires=settings.auth_jwt.access_token_lifetime_seconds,
        refresh_expires=settings.auth_jwt.refresh_token_lifetime_seconds,
    )

    return TokenResponseForOAuth2(
        access_token=access_token,
        token_type="bearer",
    )


def verify_telegram_auth(
    telegram_data: dict,
    bot_token: str = settings.telegram.bot_token,
) -> dict:
    data = telegram_data.copy()

    ensure_hash_exists(data)
    validate_telegram_hash(data, bot_token)

    auth_date = int(data.get("auth_date", 0))
    validate_auth_date(auth_date)

    return data


async def authenticate_via_telegram(
    session: AsyncSession,
    raw_data: dict,
) -> User:
    verified_data = verify_telegram_auth(raw_data)
    telegram_user = TelegramUserData(**verified_data)

    user = await get_user_by_telegram_id(session, telegram_user.id)
    if not user:
        user = await create_user_via_telegram(session, telegram_user)

    return user
