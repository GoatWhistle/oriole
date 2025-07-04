from shared.exceptions import NotFoundException


class SpaceNotFoundException(NotFoundException):
    detail = "Space not found"
