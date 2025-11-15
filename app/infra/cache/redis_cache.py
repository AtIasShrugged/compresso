"""Redis cache provider implementation."""
import json
from typing import Optional
from datetime import datetime
import redis.asyncio as aioredis
from loguru import logger
from ...core.entities import SummaryResult
from ...config import settings


class RedisCache:
    """Redis-based cache provider."""
    
    def __init__(self, redis_url: str | None = None):
        self.redis_url = redis_url or settings.redis_url
        self.max_items = settings.cache_max_items
        self._client: Optional[aioredis.Redis] = None
        self.recent_zset_key = "summary:recent"
    
    async def connect(self) -> None:
        """Establish Redis connection."""
        if self._client is None:
            self._client = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Verify Redis is available
            await self._client.ping()
            logger.info(f"Connected to Redis: {self.redis_url}")
    
    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("Disconnected from Redis")
    
    def _make_key(self, key: str) -> str:
        """Make full Redis key."""
        return f"summary:{key}"
    
    async def get(self, key: str) -> Optional[SummaryResult]:
        """Get cached summary by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached SummaryResult or None if not found
        """
        await self.connect()
        
        try:
            data = await self._client.get(self._make_key(key))
            if data:
                return SummaryResult(**json.loads(data))
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    async def set(self, key: str, value: SummaryResult, add_to_history: bool = False) -> None:
        """Store summary in cache.
        
        Args:
            key: Cache key
            value: SummaryResult to cache
            add_to_history: If True, add to recent history list
        """
        await self.connect()
        
        try:
            # Store the summary
            data = value.model_dump_json()
            await self._client.set(self._make_key(key), data)
            
            # Only add to recent list if explicitly requested (for UUID keys only)
            if add_to_history:
                score = datetime.utcnow().timestamp()
                await self._client.zadd(self.recent_zset_key, {key: score})
                
                # Trim to max items
                await self.trim_to_limit(self.max_items)
            
            logger.info(f"Cached summary with key: {key} (history: {add_to_history})")
            
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
    
    async def list_recent(self, limit: int) -> list[SummaryResult]:
        """Get list of recent summaries.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of recent SummaryResults, newest first
        """
        await self.connect()
        
        try:
            # Get recent keys from ZSET (newest first)
            keys = await self._client.zrevrange(self.recent_zset_key, 0, limit - 1)
            
            if not keys:
                return []
            
            # Get all summaries
            summaries = []
            for key in keys:
                summary = await self.get(key)
                if summary:
                    summaries.append(summary)
            
            return summaries
            
        except Exception as e:
            logger.error(f"Error listing recent: {e}")
            return []
    
    async def trim_to_limit(self, limit: int) -> None:
        """Remove old entries beyond limit.
        
        Args:
            limit: Maximum number of entries to keep
        """
        await self.connect()
        
        try:
            # Get total count
            count = await self._client.zcard(self.recent_zset_key)
            
            if count > limit:
                # Get keys to remove (oldest ones)
                to_remove = await self._client.zrange(self.recent_zset_key, 0, count - limit - 1)
                
                # Remove from ZSET
                if to_remove:
                    await self._client.zrem(self.recent_zset_key, *to_remove)
                    
                    # Remove actual summary data
                    for key in to_remove:
                        await self._client.delete(self._make_key(key))
                    
                    logger.info(f"Trimmed {len(to_remove)} old cache entries")
                    
        except Exception as e:
            logger.error(f"Error trimming cache: {e}")
    
    async def delete(self, key: str) -> None:
        """Delete summary from cache.
        
        Args:
            key: Cache key
        """
        await self.connect()
        
        try:
            # Remove from ZSET
            await self._client.zrem(self.recent_zset_key, key)
            
            # Remove actual data
            await self._client.delete(self._make_key(key))
            
            logger.info(f"Deleted cache entry: {key}")
            
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")


# Global cache instance
redis_cache = RedisCache()
