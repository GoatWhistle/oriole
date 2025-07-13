from starlette import status

from shared.exceptions import AppException


class AccountNotFoundError(AppException):
    detail = "Account not found"
    status_code = status.HTTP_404_NOT_FOUND


class InvalidMessageIdException(AppException):
    detail = "Invalid message id"
    status_code = status.HTTP_400_BAD_REQUEST


class MessageNotFoundOrForbiddenException(AppException):
    detail = "Message not found"
    status_code = status.HTTP_403_FORBIDDEN


class ChatAlreadyExistsException(AppException):
    detail = "Chat already exists"
    status_code = status.HTTP_400_BAD_REQUEST
