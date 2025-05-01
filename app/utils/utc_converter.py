from datetime import datetime

from pytz import tzinfo, UTC


def to_utc(datetime_in: datetime, user_tz: tzinfo.BaseTzInfo) -> datetime:
    if datetime_in.tzinfo is None:
        localized_dt = user_tz.localize(datetime_in)
    else:
        localized_dt = datetime_in.astimezone(user_tz)
    return localized_dt.astimezone(UTC)
