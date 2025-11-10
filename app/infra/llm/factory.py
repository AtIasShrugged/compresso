"""LLM client factory."""
from .openai_client import OpenAIClient
from .anthropic_client import AnthropicClient


class LLMFactory:
    """Factory for creating LLM clients based on model prefix."""
    
    @staticmethod
    def get_client(model: str):
        """Get LLM client based on model prefix.
        
        Args:
            model: Model string in format "provider:model"
            
        Returns:
            LLM client instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider = model.split(":", 1)[0] if ":" in model else "openai"
        
        if provider == "openai":
            return OpenAIClient()
        elif provider == "anthropic":
            return AnthropicClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


# Global factory instance
llm_factory = LLMFactory()
