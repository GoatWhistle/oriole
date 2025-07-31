from shared.exceptions import InactiveObjectException, RuleException


class TaskInactiveException(InactiveObjectException):
    detail: str = "Operation is not allowed on inactive task."


class TaskAlreadySolved(RuleException):
    detail: str = "Task has already been solved"


class TaskCounterLimitExceededException(RuleException):
    detail: str = (
        "The number of user attempts is more than the number of maximum attempts of task"
    )


class TestIsNotPublic(RuleException):
    detail: str = "Test is not public"


class InvalidStringMatchTaskWithNumberConfiguration(RuleException):
    detail: str = "If compare_as_number is True, other options must be None"


class InvalidStringMatchTaskWithStringConfiguration(RuleException):
    detail: str = (
        "If compare_as_number is False, string comparison options must be explicitly set"
    )
