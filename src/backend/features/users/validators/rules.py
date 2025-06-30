from features.users.exceptions import (
    UserNotFoundException,
    UserInactiveException,
    UserUnverifiedException,
)
from features.users.schemas import UserAuthRead


async def validate_activity_and_verification(user_from_db: UserAuthRead):
    if not user_from_db:
        raise UserNotFoundException()

    if not user_from_db.is_active:
        raise UserInactiveException()

    if not user_from_db.is_verified:
        raise UserUnverifiedException()
