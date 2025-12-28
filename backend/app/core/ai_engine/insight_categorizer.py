"""Insight categorizer for prioritization and classification."""

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


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


class InsightCategorizer:
    """Categorize and prioritize insights."""

    async def categorize(
        self,
        raw_insights: list[Any],
        profile_result: Any,
        goal_type: str,
    ) -> list[CategorizedInsight]:
        """Categorize insights with proper types and priorities.

        Args:
            raw_insights: Parsed insights from Claude
            profile_result: Profiling results for context
            goal_type: User's analysis goal

        Returns:
            Categorized and prioritized insights
        """
        categorized = []

        logger.info(f"Categorizing {len(raw_insights)} insights for goal '{goal_type}'")

        for raw in raw_insights:
            # Detect insight type from description
            insight_type = self._detect_type(raw.description)

            # Calculate priority
            priority = self._calculate_priority(raw.severity, insight_type, goal_type)

            # Determine impact level
            impact = self._determine_impact(raw.severity, insight_type)

            # Extract affected columns
            affected_columns = self._extract_columns(raw.description, profile_result)

            categorized.append(
                CategorizedInsight(
                    severity=raw.severity,
                    type=insight_type,
                    description=raw.description,
                    recommendation=raw.recommendation,
                    priority=priority,
                    affected_columns=affected_columns,
                    impact=impact,
                )
            )

        # Sort by priority (lower number = higher priority)
        categorized.sort(key=lambda x: (x.priority, x.severity))

        logger.info(
            f"Categorized insights: {sum(1 for i in categorized if i.severity == 'critical')} critical, "
            f"{sum(1 for i in categorized if i.severity == 'warning')} warnings, "
            f"{sum(1 for i in categorized if i.severity == 'info')} info"
        )

        return categorized

    def _detect_type(self, description: str) -> str:
        """Detect insight type from description.

        Args:
            description: Insight description

        Returns:
            Insight type
        """
        description_lower = description.lower()

        # Check for specific patterns
        if any(
            keyword in description_lower
            for keyword in ["missing", "null", "empty", "blank"]
        ):
            return "missing_data"

        elif any(
            keyword in description_lower for keyword in ["duplicate", "repeated"]
        ):
            return "duplicates"

        elif any(keyword in description_lower for keyword in ["outlier", "anomal"]):
            return "outliers"

        elif any(
            keyword in description_lower
            for keyword in ["type", "mismatch", "inconsistent type"]
        ):
            return "data_type_mismatch"

        elif any(
            keyword in description_lower for keyword in ["pattern", "format", "structure"]
        ):
            return "pattern_violation"

        elif any(
            keyword in description_lower
            for keyword in ["correlation", "multicollinearity", "related"]
        ):
            return "quality_issue"

        elif any(
            keyword in description_lower
            for keyword in ["cardinality", "unique", "distinct"]
        ):
            return "quality_issue"

        else:
            return "quality_issue"

    def _calculate_priority(
        self,
        severity: str,
        insight_type: str,
        goal_type: str,
    ) -> int:
        """Calculate priority (1-5, lower is higher priority).

        Args:
            severity: Insight severity
            insight_type: Type of insight
            goal_type: User's analysis goal

        Returns:
            Priority number (1-5)
        """
        # Base priority from severity
        base_priority = {
            "critical": 1,
            "warning": 2,
            "info": 5,
        }.get(severity, 3)

        # Adjust based on goal type
        if goal_type == "ml_preparation":
            # Prioritize data quality issues for ML
            if insight_type in {"missing_data", "duplicates", "outliers"}:
                base_priority = max(1, base_priority - 1)

        elif goal_type == "business_reporting":
            # Prioritize consistency issues for reporting
            if insight_type in {"pattern_violation", "data_type_mismatch"}:
                base_priority = max(1, base_priority - 1)

        elif goal_type == "anomaly_detection":
            # Prioritize outliers and anomalies
            if insight_type == "outliers":
                base_priority = max(1, base_priority - 1)

        return base_priority

    def _determine_impact(self, severity: str, insight_type: str) -> str:
        """Determine impact level.

        Args:
            severity: Insight severity
            insight_type: Type of insight

        Returns:
            Impact level (High, Medium, Low)
        """
        if severity == "critical":
            return "High"

        elif severity == "warning":
            # Some warnings have higher impact
            if insight_type in {"missing_data", "duplicates"}:
                return "High"
            else:
                return "Medium"

        else:
            return "Low"

    def _extract_columns(
        self,
        description: str,
        profile_result: Any,
    ) -> list[str]:
        """Extract mentioned column names from description.

        Args:
            description: Insight description
            profile_result: Profiling results

        Returns:
            List of affected column names
        """
        columns = []

        # Extract column names mentioned in description
        for profile in profile_result.column_profiles:
            col_name = profile.column_name

            # Check if column name appears in description
            # Use word boundaries to avoid partial matches
            if f"'{col_name}'" in description or f'"{col_name}"' in description:
                columns.append(col_name)
            elif f" {col_name} " in f" {description} ":
                columns.append(col_name)

        return columns
