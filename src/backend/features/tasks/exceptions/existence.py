from shared.exceptions import NotFoundException, BadRequest


class TaskNotFoundException(NotFoundException):
    detail: str = "Task not found"


class TaskHasNoTests(BadRequest):
    detail: str = "Task has no tests"
