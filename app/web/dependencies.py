"""Dependency injection for web layer."""
from ..infra.llm import llm_factory
from ..infra.transcript import URLReader, YouTubeProvider
from ..infra.cache import redis_cache
from ..core.usecases import SummarizeUseCase


class TranscriptProviderAdapter:
    """Adapter to combine URL and YouTube providers into single interface."""
    
    def __init__(self):
        self.url_reader = URLReader()
        self.youtube_provider = YouTubeProvider()
    
    async def from_url(self, url: str) -> str:
        return await self.url_reader.from_url(url)
    
    async def from_youtube(self, video_id: str) -> tuple[str, dict]:
        return await self.youtube_provider.from_youtube(video_id)


def get_summarize_usecase(model: str) -> SummarizeUseCase:
    """Get SummarizeUseCase instance with dependencies.
    
    Args:
        model: LLM model string
        
    Returns:
        Configured SummarizeUseCase
    """
    llm_client = llm_factory.get_client(model)
    transcript_provider = TranscriptProviderAdapter()
    cache_provider = redis_cache
    
    return SummarizeUseCase(
        llm_client=llm_client,
        transcript_provider=transcript_provider,
        cache_provider=cache_provider
    )
