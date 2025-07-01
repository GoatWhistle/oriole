from datetime import datetime

from pytz import utc

from shared.exceptions import (
    RequestTimeoutException,
    InvalidTokenException,
)
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
