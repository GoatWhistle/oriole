import bcrypt
import jwt

from datetime import datetime
from pytz import utc

from asyncpg.pgproto.pgproto import timedelta

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text,
    algorithm: str = settings.auth_jwt.algorithm,
    lifetime_seconds: int = settings.auth_jwt.lifetime_seconds,
):
    to_encode = payload.copy()
    current_time_utc = datetime.now(utc)
    expire = current_time_utc + timedelta(seconds=lifetime_seconds)

    to_encode.update(
        expire=expire,
        created_at=current_time_utc,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithm=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> bytes:
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
