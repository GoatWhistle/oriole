from features.users.schemas import UserAuthRead

from features.users.exceptions import (
    UserNotFoundError,
    UserInactiveError,
    UserUnverifiedError,
)


async def validate_activity_and_verification(user_from_db: UserAuthRead):
    if not user_from_db:
        raise UserNotFoundError()

    if not user_from_db.is_active:
        raise UserInactiveError()

    if not user_from_db.is_verified:
        raise UserUnverifiedError()
