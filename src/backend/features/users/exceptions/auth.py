from fastapi import HTTPException, status


class AuthenticationRequiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )


class AuthenticatedForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authenticated users cannot perform this action",
        )


class UserInactiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
        )


class UserUnverifiedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is unverified"
        )
