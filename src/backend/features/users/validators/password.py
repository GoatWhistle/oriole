from features.users.exceptions import (
    InvalidCredentialsException,
    PasswordMatchException,
)
from utils.JWT import validate_password


def validate_password_matching(password: str, hashed_password: str) -> bool:
    if not validate_password(password=password, hashed_password=hashed_password):
        raise InvalidCredentialsException()


def validate_password_not_equal(plain_password: str, hashed_password: str) -> None:
    if validate_password(password=plain_password, hashed_password=hashed_password):
        raise PasswordMatchException()
