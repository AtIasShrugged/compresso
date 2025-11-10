"""Anthropic Claude LLM client implementation."""
from anthropic import AsyncAnthropic
from loguru import logger
from ...core.entities import SummaryOptions
from ...config import settings


class AnthropicClient:
    """Anthropic Claude LLM client."""
    
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.anthropic_api_key
        self.client = AsyncAnthropic(api_key=self.api_key)
    
    async def summarize(self, text: str, options: SummaryOptions, prompt_template: str) -> str:
        """Generate summary using Anthropic Claude.
        
        Args:
            text: Text to summarize
            options: Summarization options
            prompt_template: Prompt template with placeholders
            
        Returns:
            Generated summary text
        """
        # Extract model name from options.model (format: "anthropic:claude-3-sonnet")
        model_parts = options.model.split(":", 1)
        model_name = model_parts[1] if len(model_parts) > 1 else "claude-3-sonnet-20240229"
        
        # Format prompt with template
        prompt = prompt_template.format(content=text)
        
        try:
            logger.info(f"Calling Anthropic API with model: {model_name}")
            
            response = await self.client.messages.create(
                model=model_name,
                max_tokens=2000 if options.detail == "long" else 1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            summary = response.content[0].text
            logger.info(f"Anthropic API call successful, tokens: input={response.usage.input_tokens}, output={response.usage.output_tokens}")
            
            return summary
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise RuntimeError(f"Failed to generate summary with Anthropic: {str(e)}")
