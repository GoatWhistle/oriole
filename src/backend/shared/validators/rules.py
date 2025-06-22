from shared.exceptions import InactiveObjectException


def check_is_active(is_active: bool) -> None:
    if not is_active:
        raise InactiveObjectException()
