"""
Redis client for caching and session management
"""
import redis.asyncio as aioredis
from typing import Optional
from app.core.config import settings


class RedisClient:
    """Async Redis client wrapper"""

    def __init__(self):
        self.client: Optional[aioredis.Redis] = None

    async def connect(self):
        """Connect to Redis"""
        self.client = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
        # Test connection
        await self.client.ping()
        print(f"✓ Connected to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            print("✓ Disconnected from Redis")

    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        if not self.client:
            raise RuntimeError("Redis client not connected")
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """Set key-value pair with optional expiration"""
        if not self.client:
            raise RuntimeError("Redis client not connected")
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str):
        """Delete key"""
        if not self.client:
            raise RuntimeError("Redis client not connected")
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            raise RuntimeError("Redis client not connected")
        return await self.client.exists(key) > 0


# Global Redis client instance
redis_client = RedisClient()
