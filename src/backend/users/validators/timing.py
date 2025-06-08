from datetime import datetime

from fastapi import HTTPException, status
from pytz import utc


def check_expiration_after_redirect(
    payload: dict,
):
    current_time_utc = datetime.now(utc).timestamp()
    if not (int(current_time_utc) < int(payload.get("exp", 0))):
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="The request time has expired",
        )
