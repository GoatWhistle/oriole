from shared.exceptions import NotFoundException


class TaskNotFoundException(NotFoundException):
    detail: str = "Task not found"
