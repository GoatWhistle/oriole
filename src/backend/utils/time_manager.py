from datetime import datetime, timedelta, timezone


def get_current_utc(offset_minutes: int = 0) -> datetime:
    now = datetime.now(timezone.utc)
    if offset_minutes:
        now += timedelta(minutes=offset_minutes)
    return now
