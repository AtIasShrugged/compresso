"""Unified summarization use case."""
import hashlib
import uuid
from loguru import logger
from ..entities import SummaryOptions, SummaryResult, SummaryMode
from ..ports import LLMClient, TranscriptProvider, CacheProvider
from .prompt_loader import prompt_loader


class SummarizeUseCase:
    """Unified use case for text/URL/YouTube summarization."""
    
    def __init__(
        self,
        llm_client: LLMClient,
        transcript_provider: TranscriptProvider,
        cache_provider: CacheProvider
    ):
        self.llm_client = llm_client
        self.transcript_provider = transcript_provider
        self.cache_provider = cache_provider
    
    async def execute(self, input_data: str, options: SummaryOptions) -> SummaryResult:
        """Execute summarization.
        
        Args:
            input_data: Input text/URL/video_id depending on mode
            options: Summarization options
            
        Returns:
            SummaryResult
        """
        # Generate cache key from input and options
        cache_key = self._generate_cache_key(input_data, options)
        
        # Check cache
        cached = await self.cache_provider.get(cache_key)
        if cached:
            logger.info(f"Cache hit for key: {cache_key}")
            return cached
        
        logger.info(f"Processing {options.mode} summarization")
        
        # Get text content based on mode
        text, metadata = await self._get_content(input_data, options)
        
        # Limit text size for safety
        max_chars = 100000
        if len(text) > max_chars:
            logger.warning(f"Text too long ({len(text)} chars), truncating to {max_chars}")
            text = text[:max_chars]
        
        # Load appropriate prompt template
        prompt_template = prompt_loader.load_prompt(options.mode, options.detail, options.locale)
        
        # Generate summary
        summary_text = await self.llm_client.summarize(text, options, prompt_template)
        
        # Create result
        result = SummaryResult(
            id=str(uuid.uuid4()),
            mode=options.mode.value,
            options=options,
            input_fingerprint=cache_key,
            content_md=summary_text,
            meta=metadata
        )
        
        # Cache the result
        await self.cache_provider.set(cache_key, result)
        
        logger.info(f"Summarization completed: {result.id}")
        return result
    
    async def _get_content(self, input_data: str, options: SummaryOptions) -> tuple[str, dict]:
        """Get content based on mode.
        
        Args:
            input_data: Input text/URL/video_id
            options: Summarization options
            
        Returns:
            Tuple of (text content, metadata dict)
        """
        metadata = {}
        
        if options.mode == SummaryMode.TEXT:
            return input_data, metadata
        
        elif options.mode == SummaryMode.URL:
            text = await self.transcript_provider.from_url(input_data)
            metadata["url"] = input_data
            return text, metadata
        
        elif options.mode == SummaryMode.YOUTUBE:
            text, yt_metadata = await self.transcript_provider.from_youtube(input_data)
            metadata.update(yt_metadata)
            metadata["video_id"] = input_data
            
            # Update with_timestamps based on availability
            if yt_metadata.get("has_timestamps") and options.detail == "long":
                options.with_timestamps = True
            
            return text, metadata
        
        else:
            raise ValueError(f"Unsupported mode: {options.mode}")
    
    def _generate_cache_key(self, input_data: str, options: SummaryOptions) -> str:
        """Generate cache key from input and options.
        
        Args:
            input_data: Input text/URL/video_id
            options: Summarization options
            
        Returns:
            Cache key (hash)
        """
        # Combine input and relevant options
        key_data = f"{input_data}:{options.mode}:{options.detail}:{options.model}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]
