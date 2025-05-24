from datetime import datetime, timedelta
from pytz import utc


def get_current_utc_timestamp(offset_minutes: int = 0) -> int:
    now = datetime.now(utc)
    if offset_minutes:
        now += timedelta(minutes=offset_minutes)
    return int(now.timestamp())
