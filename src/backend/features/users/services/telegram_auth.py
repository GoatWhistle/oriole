# auth.py
from features.users.validators.telegram import (
    ensure_hash_exists,
    validate_telegram_hash,
    validate_auth_date,
)


def verify_telegram_auth(telegram_data: dict, bot_token: str) -> dict:
    data = telegram_data.copy()

    ensure_hash_exists(data)
    validate_telegram_hash(data, bot_token)

    auth_date = int(data.get("auth_date", 0))
    validate_auth_date(auth_date)

    return data
