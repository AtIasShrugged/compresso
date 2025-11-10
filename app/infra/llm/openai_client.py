"""OpenAI LLM client implementation."""
from openai import AsyncOpenAI
from loguru import logger
from ...core.entities import SummaryOptions
from ...config import settings


class OpenAIClient:
    """OpenAI LLM client."""
    
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.openai_api_key
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def summarize(self, text: str, options: SummaryOptions, prompt_template: str) -> str:
        """Generate summary using OpenAI.
        
        Args:
            text: Text to summarize
            options: Summarization options
            prompt_template: Prompt template with placeholders
            
        Returns:
            Generated summary text
        """
        # Extract model name from options.model (format: "openai:openai-4nano")
        model_parts = options.model.split(":", 1)
        model_name = model_parts[1] if len(model_parts) > 1 else "openai-4nano"
        
        # Format prompt with template
        prompt = prompt_template.format(content=text)
        
        try:
            logger.info(f"Calling OpenAI API with model: {model_name}")
            
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise and accurate summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000 if options.detail == "long" else 1000
            )
            
            summary = response.choices[0].message.content
            logger.info(f"OpenAI API call successful, tokens: {response.usage.total_tokens}")
            
            return summary
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError(f"Failed to generate summary with OpenAI: {str(e)}")
