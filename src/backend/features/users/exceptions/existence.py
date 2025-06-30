from shared.exceptions import NotFoundException


class UserNotFoundException(NotFoundException):
    detail = "Group not found"


class ProfileNotFoundException(NotFoundException):
    detail = "User profile not found"
