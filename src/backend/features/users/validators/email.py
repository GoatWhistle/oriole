from datetime import datetime

from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession

from features.users import User
from features.users.crud.user import (
    get_user_by_email,
    get_user_by_id,
)
from features.users.exceptions import (
    RequestTimeoutException,
    EmailMismatchException,
    EmailAlreadyRegisteredException,
)
from utils.JWT import decode_jwt


async def validate_email_change_token(
    token: str,
    session: AsyncSession,
) -> tuple[int, str, str]:
    payload = decode_jwt(token)

    current_time = datetime.now(utc).timestamp()
    if int(current_time) >= int(payload.get("exp", 0)):
        raise RequestTimeoutException()

    user_id = int(payload["sub"])
    old_email = payload["old_email"]
    new_email = payload["new_email"]

    if await get_user_by_email(session, new_email):
        raise EmailAlreadyRegisteredException(new_email)

    return user_id, old_email, new_email


async def validate_user_email_match(
    session: AsyncSession, user_id: int, expected_email: str
) -> User:
    user = await get_user_by_id(session, user_id)
    if user.email != expected_email:
        raise EmailMismatchException()
    return user
