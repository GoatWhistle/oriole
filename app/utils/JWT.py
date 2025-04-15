import bcrypt
import jwt
from core.config import settings


# def encode_jwt(
#     payload: dict,
#     private_key: str = settings.auth_jwt.private_key_path.read_text,
#     algorithm: str = settings.auth_jwt.algorithm,
# ):
#     encoded = jwt.encode(
#         payload,
#         private_key,
#         algorithm=algorithm,
#     )
#     return encoded
#
#
# def decode_jwt(
#     token: str | bytes,
#     public_key: str = settings.auth_jwt.public_key_path.read_text(),
#     algorithm: str = settings.auth_jwt.algorithm,
# ):
#     decoded = jwt.decode(
#         token,
#         public_key,
#         algorithm=[algorithm],
#     )
#     return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode,
        hashed_password=hashed_password,
    )
