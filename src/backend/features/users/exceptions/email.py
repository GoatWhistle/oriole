from fastapi import HTTPException, status


class EmailRequiredExceptions(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter an email",
        )


class EmailMismatchException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current email does not match token",
        )
