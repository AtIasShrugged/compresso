"""Domain entities for summarization options."""
from enum import Enum
from pydantic import BaseModel, Field


class SummaryMode(str, Enum):
    """Summarization modes."""
    TEXT = "text"
    URL = "url"
    YOUTUBE = "youtube"


class DetailLevel(str, Enum):
    """Detail level for summaries."""
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class SummaryOptions(BaseModel):
    """Options for summarization."""
    mode: SummaryMode
    detail: DetailLevel = DetailLevel.MEDIUM
    model: str = Field(default="openai:gpt-4o-mini", description="LLM model in format 'provider:model'")
    with_timestamps: bool = Field(default=False, description="Include timestamps (for video)")
    locale: str = Field(default="en", description="UI locale for prompts")

    class Config:
        use_enum_values = True
