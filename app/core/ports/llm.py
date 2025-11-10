"""Port interface for LLM clients."""
from typing import Protocol
from ..entities import SummaryOptions


class LLMClient(Protocol):
    """Interface for LLM clients."""

    async def summarize(self, text: str, options: SummaryOptions, prompt_template: str) -> str:
        """Generate summary using LLM.
        
        Args:
            text: Text to summarize
            options: Summarization options
            prompt_template: Prompt template with placeholders
            
        Returns:
            Generated summary text
        """
        ...
