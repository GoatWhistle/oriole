from shared.exceptions import NotFoundException


class SolutionNotFoundException(NotFoundException):
    detail: str = "Solution not found"


class SolutionFeedbackNotFoundException(NotFoundException):
    detail: str = "Solution feedback not found"
