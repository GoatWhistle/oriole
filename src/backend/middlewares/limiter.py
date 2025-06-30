from slowapi import Limiter
from slowapi.util import get_remote_address
from core.config import settings
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.redis.port}:{settings.redis.port}/0",
    enabled=settings.redis.limiter_enabled,
    strategy=settings.redis.limiter_strategy,
    default_limits=[
        limit.strip() for limit in settings.redis.limiter_default.split(",")
    ],
    storage_options=settings.redis.safe_storage_options,
    auto_check=False,
)


async def universal_rate_limit_handler(_: Request, exc: Exception):
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "retry_after": getattr(exc, "retry_after", 60),
            },
            headers={"Retry-After": str(getattr(exc, "retry_after", 60))},
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "type": type(exc).__name__},
    )
