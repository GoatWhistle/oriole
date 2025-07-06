from enum import Enum


class SolutionStatusEnum(str, Enum):
    SUBMITTING = "submitting"
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
