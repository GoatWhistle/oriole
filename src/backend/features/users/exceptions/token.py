from fastapi import HTTPException, status


class InvalidTokenException(HTTPException):
    def __init__(self, reason: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token invalid ({reason})"
        )


class RequestTimeoutException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="The request time has expired",
        )


class MissingTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing"
        )
