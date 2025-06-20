from fastapi import HTTPException, status

from features.groups.schemas import AccountRole


def check_user_is_member(
    role: int,
    user_id: int,
) -> None:
    if role != AccountRole.MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} do not have a MEMBER role.",
        )


def check_user_is_admin(
    role: int,
    user_id: int,
) -> None:
    if role != AccountRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} do not have a ADMIN role.",
        )


def check_user_is_owner(
    role: int,
    user_id: int,
) -> None:
    if role != AccountRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} do not have a OWNER role.",
        )


def check_user_is_admin_or_owner(
    role: int,
    user_id: int,
) -> None:
    if role not in (AccountRole.ADMIN, AccountRole.OWNER):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} do not have a ADMIN or OWNER role.",
        )
