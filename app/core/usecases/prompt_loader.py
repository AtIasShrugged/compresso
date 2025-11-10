"""Prompt template loader."""
from pathlib import Path
from loguru import logger
from ..entities import SummaryMode, DetailLevel


class PromptLoader:
    """Loads prompt templates for different modes and detail levels."""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
    
    def load_prompt(self, mode: SummaryMode, detail: DetailLevel, locale: str) -> str:
        """Load prompt template.
        
        Args:
            mode: Summarization mode
            detail: Detail level
            locale: Locale code
            
        Returns:
            Prompt template string
        """
        # Build filename: mode_detail.txt (e.g., "text_short.txt")
        filename = f"{mode.value}_{detail.value}.txt"
        filepath = self.prompts_dir / locale / filename
        
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error loading prompt {filepath}: {e}")
        
        # Fallback to default English prompt
        if locale != "en":
            filepath = self.prompts_dir / "en" / filename
            if filepath.exists():
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception as e:
                    logger.error(f"Error loading fallback prompt {filepath}: {e}")
        
        # Final fallback: generic prompt
        return self._get_default_prompt(mode, detail)
    
    def _get_default_prompt(self, mode: SummaryMode, detail: DetailLevel) -> str:
        """Get default prompt as fallback."""
        detail_map = {
            DetailLevel.SHORT: "brief",
            DetailLevel.MEDIUM: "moderate",
            DetailLevel.LONG: "detailed"
        }
        
        detail_desc = detail_map[detail]
        
        if mode == SummaryMode.YOUTUBE:
            if detail == DetailLevel.LONG:
                return """Create a detailed, structured video summary.
• At the beginning of each point, indicate the timestamp in [mm:ss] format.
• Format as a bulleted list with emojis.
• Avoid word-for-word retelling, highlight semantic blocks and conclusions.

Transcript text:
{content}"""
            else:
                return f"Create a {detail_desc} summary of the following video transcript:\n\n{{content}}"
        else:
            return f"Create a {detail_desc} summary of the following text:\n\n{{content}}"


# Global prompt loader instance
prompt_loader = PromptLoader()
