"""Port interface for cache providers."""
from typing import Protocol, Optional
from ..entities import SummaryResult


class CacheProvider(Protocol):
    """Interface for cache providers."""

    async def get(self, key: str) -> Optional[SummaryResult]:
        """Get cached summary by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached SummaryResult or None if not found
        """
        ...

    async def set(self, key: str, value: SummaryResult, add_to_history: bool = False) -> None:
        """Store summary in cache.
        
        Args:
            key: Cache key
            value: SummaryResult to cache
            add_to_history: If True, add to recent history list
        """
        ...

    async def list_recent(self, limit: int) -> list[SummaryResult]:
        """Get list of recent summaries.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of recent SummaryResults, newest first
        """
        ...

    async def trim_to_limit(self, limit: int) -> None:
        """Remove old entries beyond limit.
        
        Args:
            limit: Maximum number of entries to keep
        """
        ...

    async def delete(self, key: str) -> None:
        """Delete summary from cache.
        
        Args:
            key: Cache key
        """
        ...
