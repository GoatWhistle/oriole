from datetime import datetime

from shared.exceptions import (
    StartTimeInPastException,
    EndTimeInPastException,
    EndTimeBeforeStartTimeException,
)
from utils import get_current_utc


def check_start_time_not_in_past(start_datetime: datetime) -> None:
    if start_datetime < get_current_utc():
        raise StartTimeInPastException()


def check_end_time_not_in_past(end_datetime: datetime) -> None:
    if end_datetime < get_current_utc():
        raise EndTimeInPastException()


def check_end_time_is_after_start_time(
    start_datetime: datetime,
    end_datetime: datetime,
) -> None:
    if start_datetime >= end_datetime:
        raise EndTimeBeforeStartTimeException()
