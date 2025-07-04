import hashlib
import inspect

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.redis import redis_connection
from logging import getLogger


logger = getLogger("redis")


class AutoCacheMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        ttl: int = 600,
        exclude_paths: list[str] = None,
        invalidate_paths: list[str] = None,
    ):
        super().__init__(app)
        self.ttl = ttl
        self.exclude_paths = exclude_paths or []
        self.invalidate_paths = invalidate_paths or []
        self.redis = redis_connection.redis

    def make_cache_key(self, request: Request) -> str:
        query = str(sorted(request.query_params.items()))
        return (
            "cache:" + hashlib.sha256((request.url.path + query).encode()).hexdigest()
        )

    def make_tag_key(self, path: str) -> str:
        path = path.replace("/api/", "")
        segments = [segment for segment in path.split("/") if segment]
        return f"tag:{segments[0]}" if segments else "tag:root"

    async def cache_set(self, key: str, tag: str, value: str):
        try:
            await self.redis.setex(key, self.ttl, value)
            await self.redis.sadd(tag, key)
        except Exception as e:
            logger.error(
                f"Redis get error in {inspect.currentframe().f_code.co_name}: {e}"
            )

    async def invalidate_tag(self, tag_key: str):
        try:
            keys = await self.redis.smembers(tag_key)
            if keys:
                await self.redis.delete(*keys)
            await self.redis.delete(tag_key)
        except Exception as e:
            logger.error(
                f"Redis get error in {inspect.currentframe().f_code.co_name}: {e}"
            )

    def is_excluded(self, path: str) -> bool:
        return any(
            path.startswith(f"/api/{ex}") or path.startswith(f"{ex}")
            for ex in self.exclude_paths
        )

    def is_invalidated(self, path: str) -> bool:
        return any(
            path.startswith(f"/api/{ex}") or path.startswith(f"{ex}")
            for ex in self.invalidate_paths
        )

    async def invalidate_all_cache(self):
        try:
            cache_keys = await self.redis.keys("cache:*")
            tag_keys = await self.redis.keys("tag:*")

            if cache_keys:
                await self.redis.delete(*cache_keys)
            if tag_keys:
                await self.redis.delete(*tag_keys)
        except Exception as e:
            logger.error(
                f"Redis get error in {inspect.currentframe().f_code.co_name}: {e}"
            )

    async def dispatch(self, request: Request, call_next):
        method = request.method.upper()
        path = request.url.path

        if self.is_excluded(path):
            return await call_next(request)

        if self.is_invalidated(path):
            await self.invalidate_all_cache()

        tag_key = self.make_tag_key(path)

        if method == "GET":
            cache_key = self.make_cache_key(request)
            try:
                cached = await self.redis.get(cache_key)
            except Exception as e:
                logger.error(
                    f"Redis get error in {inspect.currentframe().f_code.co_name}: {e}"
                )
                cached = None
            if cached:
                return Response(content=cached.encode(), media_type="application/json")

            response = await call_next(request)

            if "application/json" not in response.headers.get("content-type", ""):
                return response

            body = [chunk async for chunk in response.body_iterator]
            full_body = b"".join(body)

            await self.cache_set(cache_key, tag_key, full_body.decode())
            return Response(
                content=full_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type="application/json",
            )

        elif method in {"POST", "PUT", "DELETE", "PATCH"}:
            await self.invalidate_tag(tag_key)
            return await call_next(request)

        return await call_next(request)
