from shared.exceptions import NotFoundException


class SolutionNotFoundException(NotFoundException):
    detail: str = "Solution not found"
