import hmac
import hashlib
import time

from core.config import settings
from features.users.exceptions import (
    MissingHashException,
    InvalidHashException,
    ExpiredAuthException,
)


def ensure_hash_exists(telegram_data: dict) -> None:
    if "hash" not in telegram_data:
        raise MissingHashException()


def validate_telegram_hash(telegram_data: dict, bot_token: str) -> None:
    received_hash = telegram_data["hash"]
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(telegram_data.items()) if k != "hash"
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise InvalidHashException()


def validate_auth_date(auth_date: int) -> None:
    if time.time() - auth_date > settings.telegram.registration_lifetime_seconds:
        raise ExpiredAuthException()
