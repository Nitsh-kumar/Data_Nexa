"""Data models for AI engine."""

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class RawInsight:
    """Parsed insight from Claude response."""

    severity: str
    description: str
    recommendation: str


@dataclass
class CategorizedInsight:
    """Categorized insight with priority and metadata."""

    severity: str
    type: str
    description: str
    recommendation: str
    priority: int
    affected_columns: list[str]
    impact: str
    code_suggestion: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return asdict(self)


class TokenUsageTracker:
    """Track Claude API token usage for cost monitoring."""

    def __init__(self) -> None:
        """Initialize token usage tracker."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def add(self, input_tokens: int, output_tokens: int) -> None:
        """Add token usage from an API call.

        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
        """
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    def get_cost(self) -> float:
        """Calculate approximate cost in USD.

        Returns:
            Estimated cost based on Claude Sonnet pricing
        """
        # Claude Sonnet pricing (approximate)
        input_cost = self.total_input_tokens * 0.003 / 1000
        output_cost = self.total_output_tokens * 0.015 / 1000
        return round(input_cost + output_cost, 4)

    def get_stats(self) -> dict[str, Any]:
        """Get token usage statistics.

        Returns:
            Dictionary with token counts and cost
        """
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "estimated_cost_usd": self.get_cost(),
        }

    def reset(self) -> None:
        """Reset token counters."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
