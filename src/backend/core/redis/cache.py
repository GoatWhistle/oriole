import hashlib
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .redis_connection import redis_connection


class AutoCacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ttl: int = 600, exclude_paths: list[str] = None):
        super().__init__(app)
        self.ttl = ttl
        self.exclude_paths = exclude_paths or []

    def make_cache_key(self, request: Request) -> str:
        query = str(sorted(request.query_params.items()))
        return "cache:" + hashlib.sha256((request.url.path + query).encode()).hexdigest()

    def make_tag_key(self, path: str) -> str:
        return f"tag:{path}"

    async def cache_set(self, key: str, tag: str, value: str):
        await redis_connection.redis.setex(key, self.ttl, value)
        await redis_connection.redis.sadd(tag, key)

    async def invalidate_tag(self, tag_key: str):
        keys = await redis_connection.redis.smembers(tag_key)
        if keys:
            await redis_connection.redis.delete(*keys)
        await redis_connection.redis.delete(tag_key)

    def is_excluded(self, path: str) -> bool:
        return any(path in ex.split("/") for ex in self.exclude_paths)

    async def dispatch(self, request: Request, call_next):
        method = request.method.upper()
        path = request.url.path

        if self.is_excluded(path):
            return await call_next(request)

        tag_key = self.make_tag_key(path)

        if method == "GET":
            cache_key = self.make_cache_key(request)
            cached = await redis_connection.redis.get(cache_key)
            if cached:
                return Response(content=cached, media_type="application/json")

            response = await call_next(request)

            if "application/json" not in response.headers.get("content-type", ""):
                return response

            body = [chunk async for chunk in response.body_iterator]
            full_body = b"".join(body)

            await self.cache_set(cache_key, tag_key, full_body.decode())
            return Response(content=full_body, status_code=response.status_code,
                            headers=dict(response.headers), media_type="application/json")

        elif method in {"POST", "PUT", "DELETE"}:
            await self.invalidate_tag(tag_key)
            return await call_next(request)

        return await call_next(request)
