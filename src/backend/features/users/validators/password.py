from utils.JWT import validate_password

from features.users.exceptions import InvalidCredentialsError, PasswordMatchError


def validate_password_matching(password: str, hashed_password: str) -> bool:
    if not validate_password(password=password, hashed_password=hashed_password):
        raise InvalidCredentialsError()


def validate_password_not_equal(plain_password: str, hashed_password: str) -> None:
    if validate_password(password=plain_password, hashed_password=hashed_password):
        raise PasswordMatchError()
