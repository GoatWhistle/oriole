from slowapi import Limiter
from slowapi.util import get_remote_address
from core.config import settings
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis.full_url,
    enabled=settings.redis.limiter_enabled,
    strategy=settings.redis.limiter_strategy,
    default_limits=[limit.strip() for limit in settings.redis.limiter_default.split(",")],
    # storage_options={
    #     "socket_connect_timeout": settings.redis.socket_timeout,
    #     "ssl": settings.redis.url.startswith("rediss://")
    # }
)

async def custom_rate_limit_handler(_: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded"},
        headers={"Retry-After": "60"}
    )