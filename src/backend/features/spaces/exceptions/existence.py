from shared.exceptions import NotFoundException


class SpaceNotFoundException(NotFoundException):
    detail = "Space not found"


class SpaceJoinRequestNotFoundException(NotFoundException):
    detail = "Space join request not found"
