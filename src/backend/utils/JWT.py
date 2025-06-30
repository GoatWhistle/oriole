from datetime import datetime, timedelta

import bcrypt
import jwt
from pytz import utc

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def create_email_confirmation_token(
    user_id: int,
    user_email: str,
    lifetime_seconds: int = settings.auth_jwt.email_token_lifetime_seconds,
) -> str:
    current_time_utc = datetime.now(utc)
    expire = current_time_utc + timedelta(seconds=lifetime_seconds)
    jwt_payload = {
        "sub": str(user_id),
        "email": user_email,
        "exp": expire,
        "iat": current_time_utc,
        "purpose": "email_confirmation",
    }
    return encode_jwt(payload=jwt_payload)


def create_email_update_token(
    user_id: int,
    old_email: str,
    new_email: str,
    lifetime_seconds: int = settings.auth_jwt.email_token_lifetime_seconds,
) -> str:
    current_time = datetime.now(utc)
    expire = current_time + timedelta(seconds=lifetime_seconds)

    payload = {
        "sub": str(user_id),
        "old_email": old_email,
        "new_email": new_email,
        "exp": expire.timestamp(),
        "iat": current_time.timestamp(),
        "purpose": "email_update",
    }

    return encode_jwt(payload=payload)


def create_password_confirmation_token(
    user_id: int,
    user_email: str,
    lifetime_seconds: int = settings.auth_jwt.password_token_lifetime_seconds,
) -> str:
    current_time_utc = datetime.now(utc)
    expire = current_time_utc + timedelta(seconds=lifetime_seconds)
    jwt_payload = {
        "sub": str(user_id),
        "email": user_email,
        "exp": expire,
        "iat": current_time_utc,
    }
    return encode_jwt(payload=jwt_payload)


def create_access_token(
    user_id: int,
    user_email: str,
    lifetime_seconds: int = settings.auth_jwt.access_token_lifetime_seconds,
) -> str:
    current_time_utc = datetime.now(utc)
    expire = current_time_utc + timedelta(seconds=lifetime_seconds)
    jwt_payload = {
        "sub": str(user_id),
        "email": user_email,
        "exp": expire,
        "iat": current_time_utc,
    }
    return encode_jwt(payload=jwt_payload)


def create_refresh_token(
    user_id: int,
    user_email: str,
    lifetime_seconds: int = settings.auth_jwt.refresh_token_lifetime_seconds,
) -> str:
    current_time_utc = datetime.now(utc)
    expire = current_time_utc + timedelta(seconds=lifetime_seconds)
    jwt_payload = {
        "sub": str(user_id),
        "email": user_email,
        "exp": expire,
        "iat": current_time_utc,
    }
    return encode_jwt(payload=jwt_payload)


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )


def get_current_token_payload(
    token: str,
) -> dict:
    if token.startswith("Bearer "):
        token = token[7:]

    payload = decode_jwt(token=token)
    return payload
