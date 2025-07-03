from fastapi import HTTPException
from starlette import status


class AccountNotFoundError(HTTPException):
    def __init__(self, detail: str = "Account not found for current user"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
