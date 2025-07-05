from slowapi import Limiter
from slowapi.util import get_remote_address
from core.config import (
    RateLimiterSettings,
    settings,
)
from shared.exceptions.limits import (
    RateLimitException,
    LimiterException,
)
from fastapi.responses import JSONResponse
from fastapi import Request


def create_limiter(limiter_settings: RateLimiterSettings) -> Limiter | None:
    if not limiter_settings.enabled:
        return None

    storage_config = limiter_settings.get_storage_config()
    storage_options = storage_config.get_storage_options()

    return Limiter(
        key_func=get_remote_address,
        storage_uri=storage_config.get_storage_uri(),
        strategy=limiter_settings.strategy,
        default_limits=[limit.strip() for limit in limiter_settings.default.split(",")],
        storage_options=storage_options,
        auto_check=False,
    )


rate_limiter_settings = settings.rate_limiter

limiter = create_limiter(rate_limiter_settings)


async def handle_rate_limit_exceeded(_: Request, exc: RateLimitException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "retry_after": exc.retry_after},
        headers={"Retry-After": str(exc.retry_after)},
    )


async def handle_limiter_exception(_: Request, exc: LimiterException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": type(exc).__name__},
    )
