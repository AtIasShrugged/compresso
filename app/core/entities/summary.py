"""Domain entities for summary results."""
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field
from .options import SummaryOptions


class SummaryResult(BaseModel):
    """Result of summarization."""
    id: str = Field(description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    mode: str = Field(description="Summarization mode")
    options: SummaryOptions
    input_fingerprint: str = Field(description="Hash of input for deduplication")
    content_md: str = Field(description="Summary content in Markdown")
    source: Optional[str] = Field(default=None, description="Source URL: article URL or video link")
    meta: dict[str, Any] = Field(default_factory=dict, description="Additional metadata (duration, timestamps, etc.)")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
