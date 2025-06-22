from shared.exceptions import RoleException


class UserNotMemberException(RoleException):
    detail = "User does not have MEMBER role."


class UserNotAdminException(RoleException):
    detail = "User does not have ADMIN role."


class UserNotOwnerException(RoleException):
    detail = "User does not have OWNER role."


class UserNotAdminOrOwnerException(RoleException):
    detail = "User does not have ADMIN or OWNER role."
