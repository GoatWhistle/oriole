from fastapi import HTTPException, status
from utils.JWT import validate_password


def validate_password_matching(
    password: str,
    hashed_password: str,
) -> bool:
    if not validate_password(password=password, hashed_password=hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )
