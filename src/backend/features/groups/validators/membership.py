from features.accounts.schemas import AccountRole
from features.groups.exceptions import (
    UserNotMemberException,
    UserNotAdminException,
    UserNotOwnerException,
    UserNotAdminOrOwnerException,
)


def check_user_is_member(
    role: int,
) -> None:
    if role != AccountRole.MEMBER:
        raise UserNotMemberException()


def check_user_is_admin(
    role: int,
) -> None:
    if role != AccountRole.ADMIN:
        raise UserNotAdminException()


def check_user_is_owner(
    role: int,
) -> None:
    if role != AccountRole.OWNER:
        raise UserNotOwnerException()


def check_user_is_admin_or_owner(
    role: int,
) -> None:
    if role not in (AccountRole.ADMIN, AccountRole.OWNER):
        raise UserNotAdminOrOwnerException()
