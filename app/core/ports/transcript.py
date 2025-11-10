"""Port interface for transcript providers."""
from typing import Protocol


class TranscriptProvider(Protocol):
    """Interface for transcript/text extraction providers."""

    async def from_url(self, url: str) -> str:
        """Extract text from article URL.
        
        Args:
            url: Article URL
            
        Returns:
            Extracted article text
        """
        ...

    async def from_youtube(self, video_id: str) -> tuple[str, dict]:
        """Get transcript from YouTube video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Tuple of (transcript text, metadata dict with timestamps)
        """
        ...
