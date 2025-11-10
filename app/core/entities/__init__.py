"""Core domain entities."""
from .options import SummaryOptions, SummaryMode, DetailLevel
from .summary import SummaryResult

__all__ = [
    "SummaryOptions",
    "SummaryMode",
    "DetailLevel",
    "SummaryResult",
]
