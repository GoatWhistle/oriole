from fastapi import HTTPException
from starlette import status


class AccountNotFoundError(HTTPException):
    def __init__(self, detail: str = "Account not found for current user"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidMessageIdException(Exception):
    def __init__(self, message_id: int):
        self.message = f"Invalid message_id: {message_id}"
        super().__init__(self.message)


class MessageNotFoundOrForbiddenException(Exception):
    def __init__(self, message_id: int):
        self.message = f"Message with id {message_id} not found or permission denied"
        super().__init__(self.message)
