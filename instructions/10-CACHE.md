# CacheProvider Interface

```python
class CacheProvider(Protocol):
    async def get(self, key: str) -> SummaryResult | None: ...
    async def set(self, key: str, value: SummaryResult) -> None: ...
    async def list_recent(self, limit: int) -> list[SummaryResult]: ...
    async def trim_to_limit(self, limit: int) -> None: ...
```

## Redis Implementation

- **Key**: `summary:{hash(input+options)}`.
- **List**: ZSET `summary:recent` with score = timestamp.
- On **set**: ZADD, TRIM (remove beyond `CACHE_MAX_ITEMS`).
- For **/history** view: ZREVRANGE → MGET.
