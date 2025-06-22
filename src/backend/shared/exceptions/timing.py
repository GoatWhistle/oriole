from shared.exceptions import AppException


class TimingException(AppException):
    detail: str = "Timing validation error"


class StartTimeInPastException(TimingException):
    detail: str = "Start time cannot be in the past."


class EndTimeInPastException(TimingException):
    detail: str = "End time cannot be in the past."


class EndTimeBeforeStartTimeException(TimingException):
    detail: str = "End time must be after start time."
