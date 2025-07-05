import redis.asyncio as redis
from core.config import settings


class RedisConnection:
    def __init__(self, url: str):
        self.url = url
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(self.url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.aclose()


redis_connection = RedisConnection(settings.redis.get_storage_uri())
