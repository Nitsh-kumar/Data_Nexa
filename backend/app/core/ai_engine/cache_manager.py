"""Cache manager for AI responses using Redis."""

import hashlib
import json
import logging
from typing import Any

import redis.asyncio as redis

from app.config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Manage caching of AI responses."""

    def __init__(self, redis_client: redis.Redis | None = None):
        """Initialize cache manager.

        Args:
            redis_client: Redis client instance (optional)
        """
        if redis_client:
            self.redis = redis_client
        else:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )

        self.prefix = "ai_insights:"
        self.default_ttl = settings.CACHE_TTL

        logger.info(
            f"CacheManager initialized with Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )

    async def get(self, key: str) -> list[dict[str, Any]] | None:
        """Get cached insights.

        Args:
            key: Cache key

        Returns:
            List of insights or None if not found
        """
        try:
            cache_key = f"{self.prefix}{key}"
            cached = await self.redis.get(cache_key)

            if cached:
                logger.info(f"Cache HIT for key: {key}")
                return json.loads(cached)

            logger.info(f"Cache MISS for key: {key}")
            return None

        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None

    async def set(
        self,
        key: str,
        insights: list[Any],
        ttl: int | None = None,
    ) -> None:
        """Cache insights.

        Args:
            key: Cache key
            insights: List of insights to cache
            ttl: Time to live in seconds (optional)
        """
        try:
            cache_key = f"{self.prefix}{key}"
            ttl = ttl or self.default_ttl

            # Convert insights to dict format
            insights_data = [self._insight_to_dict(i) for i in insights]

            # Store in Redis with expiration
            await self.redis.setex(
                cache_key,
                ttl,
                json.dumps(insights_data),
            )

            logger.info(f"Cached insights for key: {key} (TTL: {ttl}s)")

        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")

    async def delete(self, key: str) -> None:
        """Delete cached insights.

        Args:
            key: Cache key
        """
        try:
            cache_key = f"{self.prefix}{key}"
            await self.redis.delete(cache_key)
            logger.info(f"Deleted cache for key: {key}")

        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")

    async def clear_all(self) -> None:
        """Clear all cached insights."""
        try:
            # Find all keys with our prefix
            pattern = f"{self.prefix}*"
            keys = []

            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                await self.redis.delete(*keys)
                logger.info(f"Cleared {len(keys)} cached insights")
            else:
                logger.info("No cached insights to clear")

        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        try:
            # Count keys with our prefix
            pattern = f"{self.prefix}*"
            count = 0

            async for _ in self.redis.scan_iter(match=pattern):
                count += 1

            # Get Redis info
            info = await self.redis.info("stats")

            return {
                "cached_insights_count": count,
                "redis_hits": info.get("keyspace_hits", 0),
                "redis_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0),
                ),
            }

        except Exception as e:
            logger.error(f"Cache stats error: {str(e)}")
            return {"error": str(e)}

    def generate_cache_key(self, analysis_id: int, profile_hash: str) -> str:
        """Generate cache key from analysis characteristics.

        Args:
            analysis_id: Analysis ID
            profile_hash: Hash of profile characteristics

        Returns:
            Cache key
        """
        key_data = f"{analysis_id}_{profile_hash}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _insight_to_dict(self, insight: Any) -> dict[str, Any]:
        """Convert insight object to dictionary.

        Args:
            insight: Insight object

        Returns:
            Dictionary representation
        """
        if hasattr(insight, "__dict__"):
            return {
                k: v
                for k, v in insight.__dict__.items()
                if not k.startswith("_")
            }
        else:
            return dict(insight)

    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate.

        Args:
            hits: Number of cache hits
            misses: Number of cache misses

        Returns:
            Hit rate as percentage
        """
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)

    async def close(self) -> None:
        """Close Redis connection."""
        try:
            await self.redis.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {str(e)}")
