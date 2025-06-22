from shared.exceptions import RuleException


class TaskAlreadySolved(RuleException):
    detail: str = "Task has already been solved"


class TaskCounterLimitExceededException(RuleException):
    detail: str = (
        "The number of user attempts is more than the number of maximum attempts of task"
    )
