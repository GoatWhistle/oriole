from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    def __init__(self, user_id: int | None = None, email: str | None = None):
        detail = "User not found"
        if user_id:
            detail = f"User {user_id} does not exist"
        elif email:
            detail = f"User with email {email} not found"

        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserAlreadyExistsError(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' is already registered",
        )


class ProfileNotFoundError(HTTPException):
    def __init__(self, user_id: int | None = None, email: str | None = None):
        detail = "User profile not found"
        if user_id:
            detail = f"UserProfile for user {user_id} does not exist"

        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
