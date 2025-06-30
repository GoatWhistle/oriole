from datetime import datetime
from pytz import utc

from utils.JWT import decode_jwt

from features.users.exceptions import (
    RequestTimeoutError,
    InvalidTokenError,
)


def check_expiration_after_redirect(payload: dict):
    current_time_utc = datetime.now(utc).timestamp()
    if not (int(current_time_utc) < int(payload.get("exp", 0))):
        raise RequestTimeoutError()


def validate_token_expiration(token: str) -> bool:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        current_time_utc = datetime.now(utc).timestamp()
        return int(current_time_utc) >= int(payload.get("exp", 0))

    except Exception as ex:
        raise InvalidTokenError(reason=str(ex)) from ex
