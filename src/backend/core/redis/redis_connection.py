import redis.asyncio as aioredis
from core.config import settings


class RedisConnection:
    def __init__(self, url: str, db: int):
        self.url = url
        self.redis = None
        self.db = db

    async def connect(self):
        self.redis = await aioredis.from_url(self.url, db=self.db)

    async def close(self):
        if self.redis:
            await self.redis.close()


redis_connection = RedisConnection(f"{settings.redis.url}{settings.redis.port}", 0)
