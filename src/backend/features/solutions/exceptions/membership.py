from shared.exceptions import RoleException


class UserNotCreatorOfSolutionException(RoleException):
    detail = "User is not the creator of this solution."
