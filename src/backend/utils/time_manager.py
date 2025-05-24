from datetime import datetime
from pytz import utc


def get_current_utc_timestamp() -> int:
    return int(datetime.now(utc).timestamp())
