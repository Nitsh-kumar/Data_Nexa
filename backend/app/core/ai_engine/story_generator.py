"""Story generator for creating plain English executive summaries."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class StoryGenerator:
    """Generate plain English executive summaries."""

    async def generate(
        self,
        profile_result: Any,
        insights: list[Any],
    ) -> str:
        """Generate executive summary.

        Args:
            profile_result: Profiling results
            insights: Generated insights

        Returns:
            Plain English summary
        """
        logger.info("Generating executive summary")

        summary_parts = []

        # Dataset description
        summary_parts.append(self._create_dataset_intro(profile_result))

        # Quality assessment
        summary_parts.append(self._create_quality_assessment(profile_result))

        # Issues summary
        summary_parts.append(self._create_issues_summary(insights))

        # Top issue highlight
        top_issue = self._get_top_issue(insights)
        if top_issue:
            summary_parts.append(self._create_top_issue_highlight(top_issue))

        # Positive note or next steps
        summary_parts.append(self._create_conclusion(profile_result, insights))

        summary = " ".join(summary_parts)

        logger.info(f"Generated summary with {len(summary)} characters")

        return summary

    def _create_dataset_intro(self, profile_result: Any) -> str:
        """Create dataset introduction.

        Args:
            profile_result: Profiling results

        Returns:
            Introduction text
        """
        row_count = profile_result.row_count
        col_count = profile_result.column_count

        # Format row count with commas
        row_str = f"{row_count:,}"

        # Determine dataset size description
        if row_count < 1000:
            size_desc = "small"
        elif row_count < 100000:
            size_desc = "medium-sized"
        elif row_count < 1000000:
            size_desc = "large"
        else:
            size_desc = "very large"

        return (
            f"This is a {size_desc} dataset containing {row_str} rows "
            f"and {col_count} columns."
        )

    def _create_quality_assessment(self, profile_result: Any) -> str:
        """Create quality assessment.

        Args:
            profile_result: Profiling results

        Returns:
            Quality assessment text
        """
        quality_score = profile_result.quality_score

        # Determine quality description
        if quality_score >= 90:
            quality_desc = "excellent"
            emoji = "✨"
        elif quality_score >= 80:
            quality_desc = "very good"
            emoji = "👍"
        elif quality_score >= 70:
            quality_desc = "good"
            emoji = "✓"
        elif quality_score >= 60:
            quality_desc = "fair"
            emoji = "⚠️"
        elif quality_score >= 50:
            quality_desc = "below average"
            emoji = "⚠️"
        else:
            quality_desc = "poor"
            emoji = "❌"

        return f"Overall data quality is {quality_desc} ({quality_score}/100)."

    def _create_issues_summary(self, insights: list[Any]) -> str:
        """Create issues summary.

        Args:
            insights: List of insights

        Returns:
            Issues summary text
        """
        # Count by severity
        critical_count = sum(1 for i in insights if i.severity == "critical")
        warning_count = sum(1 for i in insights if i.severity == "warning")
        info_count = sum(1 for i in insights if i.severity == "info")

        parts = []

        if critical_count > 0:
            if critical_count == 1:
                parts.append("There is 1 critical issue that requires immediate attention.")
            else:
                parts.append(
                    f"There are {critical_count} critical issues that require immediate attention."
                )

        if warning_count > 0:
            if critical_count > 0:
                parts.append(
                    f"Additionally, {warning_count} warning{'s' if warning_count > 1 else ''} should be reviewed."
                )
            else:
                parts.append(
                    f"There {'are' if warning_count > 1 else 'is'} {warning_count} warning{'s' if warning_count > 1 else ''} to review."
                )

        if critical_count == 0 and warning_count == 0:
            if info_count > 0:
                parts.append(
                    "No critical issues or warnings were detected. "
                    f"The analysis found {info_count} informational insight{'s' if info_count > 1 else ''}."
                )
            else:
                parts.append("No issues were detected. The data appears to be in good condition.")

        return " ".join(parts)

    def _get_top_issue(self, insights: list[Any]) -> Any | None:
        """Get the top priority issue.

        Args:
            insights: List of insights

        Returns:
            Top issue or None
        """
        # Filter to critical and warnings only
        important_insights = [
            i for i in insights if i.severity in {"critical", "warning"}
        ]

        if not important_insights:
            return None

        # Return the first one (already sorted by priority)
        return important_insights[0]

    def _create_top_issue_highlight(self, issue: Any) -> str:
        """Create highlight for top issue.

        Args:
            issue: Top issue

        Returns:
            Highlight text
        """
        severity_text = "most critical issue" if issue.severity == "critical" else "main concern"

        # Truncate description if too long
        description = issue.description
        if len(description) > 150:
            description = description[:147] + "..."

        return f"The {severity_text} is: {description}"

    def _create_conclusion(self, profile_result: Any, insights: list[Any]) -> str:
        """Create conclusion with next steps.

        Args:
            profile_result: Profiling results
            insights: List of insights

        Returns:
            Conclusion text
        """
        quality_score = profile_result.quality_score
        critical_count = sum(1 for i in insights if i.severity == "critical")
        warning_count = sum(1 for i in insights if i.severity == "warning")

        if quality_score >= 85 and critical_count == 0:
            return (
                "The data is ready for analysis with minimal preprocessing required. "
                "Consider reviewing the recommendations to further optimize data quality."
            )

        elif critical_count > 0:
            return (
                "Address the critical issues before proceeding with analysis to ensure reliable results. "
                "Review the detailed recommendations for specific actions to take."
            )

        elif warning_count > 0:
            return (
                "Review and address the warnings to improve data quality. "
                "The data can be used for analysis, but addressing these issues will improve results."
            )

        else:
            return (
                "The data is in good condition. "
                "Review the insights for opportunities to enhance data quality."
            )

    def generate_short_summary(self, profile_result: Any) -> str:
        """Generate a short one-line summary.

        Args:
            profile_result: Profiling results

        Returns:
            Short summary
        """
        quality_score = profile_result.quality_score
        row_count = profile_result.row_count
        col_count = profile_result.column_count

        if quality_score >= 85:
            status = "excellent condition"
        elif quality_score >= 70:
            status = "good condition"
        elif quality_score >= 50:
            status = "fair condition"
        else:
            status = "needs improvement"

        return (
            f"{row_count:,} rows × {col_count} columns | "
            f"Quality: {quality_score}/100 ({status})"
        )
