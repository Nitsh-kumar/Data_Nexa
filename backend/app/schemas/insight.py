"""Pydantic schemas for insights."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class InsightSeverity(str, Enum):
    """Insight severity levels."""

    CRITICAL = "critical"
    HIGH = "warning"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class InsightType(str, Enum):
    """Insight types."""

    MISSING_DATA = "missing_data"
    OUTLIERS = "outliers"
    DUPLICATES = "duplicates"
    DATA_TYPE_MISMATCH = "data_type_mismatch"
    PATTERN_VIOLATION = "pattern_violation"
    QUALITY_ISSUE = "quality_issue"


class InsightBase(BaseModel):
    """Base insight schema."""

    severity: InsightSeverity
    type: InsightType
    description: str
    recommendation: str


class InsightCreate(InsightBase):
    """Schema for creating an insight."""

    analysis_id: int
    code_suggestion: str | None = None


class InsightUpdate(BaseModel):
    """Schema for updating an insight."""

    severity: InsightSeverity | None = None
    type: InsightType | None = None
    description: str | None = None
    recommendation: str | None = None
    code_suggestion: str | None = None


class InsightResponse(InsightBase):
    """Schema for insight response."""

    id: int
    analysis_id: int
    code_suggestion: str | None = None
    priority: int = Field(default=3, ge=1, le=5)
    affected_columns: list[str] = Field(default_factory=list)
    impact: str = Field(default="Medium")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InsightListResponse(BaseModel):
    """Schema for paginated insight list."""

    items: list[InsightResponse]
    total: int
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    pages: int

    @property
    def has_next(self) -> bool:
        """Check if there are more pages."""
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        """Check if there are previous pages."""
        return self.page > 1


class InsightSummary(BaseModel):
    """Summary of insights by severity."""

    critical_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    total_count: int = 0
    executive_summary: str | None = None


class TokenUsageStats(BaseModel):
    """Token usage statistics."""

    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class CacheStats(BaseModel):
    """Cache statistics."""

    cached_insights_count: int
    redis_hits: int
    redis_misses: int
    hit_rate: float
