from sqlalchemy.ext.asyncio import AsyncSession
from utils.JWT import decode_jwt
from datetime import datetime
from pytz import utc
from features.users.exceptions import (
    RequestTimeoutError,
    EmailMismatchError,
    EmailAlreadyExistsError,
)

from features.users.crud.user import (
    get_user_by_email,
    get_user_by_id,
)
from features.users import User


async def validate_email_change_token(
    token: str,
    session: AsyncSession,
) -> tuple[int, str, str]:
    payload = decode_jwt(token)

    current_time = datetime.now(utc).timestamp()
    if int(current_time) >= int(payload.get("exp", 0)):
        raise RequestTimeoutError()

    user_id = int(payload["sub"])
    old_email = payload["old_email"]
    new_email = payload["new_email"]

    if await get_user_by_email(session, new_email):
        raise EmailAlreadyExistsError(new_email)

    return user_id, old_email, new_email


async def validate_user_email_match(
    session: AsyncSession, user_id: int, expected_email: str
) -> User:
    user = await get_user_by_id(session, user_id)
    if user.email != expected_email:
        raise EmailMismatchError()
    return user
