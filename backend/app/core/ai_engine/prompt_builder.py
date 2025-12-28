"""Prompt builder for context-aware Claude API prompts."""

import logging
from pathlib import Path
from typing import Any

from app.core.ai_engine.anonymizer import DataAnonymizer

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Build context-aware prompts for Claude API."""

    def __init__(self, anonymizer: DataAnonymizer | None = None):
        """Initialize prompt builder.

        Args:
            anonymizer: Data anonymizer instance
        """
        self.anonymizer = anonymizer or DataAnonymizer()
        self.templates = self._load_templates()
        logger.info("PromptBuilder initialized with templates")

    async def build(
        self,
        profile_result: Any,
        goal_type: str,
    ) -> str:
        """Build prompt from profiling results.

        Args:
            profile_result: Complete profiling results
            goal_type: User's analysis goal

        Returns:
            Formatted prompt string
        """
        # Select appropriate template
        template_key = self._get_template_key(goal_type)
        template = self.templates.get(template_key, self.templates["general"])

        # Prepare dataset summary
        dataset_summary = self._create_dataset_summary(profile_result)

        # Prepare issues summary
        issues_summary = self._create_issues_summary(profile_result)

        # Anonymize sample data (first 5 columns)
        sample_columns = profile_result.column_profiles[:5]
        sample_data = await self.anonymizer.anonymize(sample_columns)

        # Format prompt
        prompt = template.format(
            dataset_summary=dataset_summary,
            issues_summary=issues_summary,
            sample_data=sample_data,
            quality_score=profile_result.quality_score,
            goal=goal_type,
        )

        logger.info(f"Built prompt for goal '{goal_type}' with length {len(prompt)}")

        return prompt

    def _get_template_key(self, goal_type: str) -> str:
        """Map goal type to template key.

        Args:
            goal_type: Analysis goal type

        Returns:
            Template key
        """
        goal_mapping = {
            "ml_preparation": "ml",
            "business_reporting": "business",
            "anomaly_detection": "anomaly",
            "data_quality": "general",
            "exploratory": "general",
        }
        return goal_mapping.get(goal_type, "general")

    def _create_dataset_summary(self, profile_result: Any) -> str:
        """Create human-readable dataset summary.

        Args:
            profile_result: Profiling results

        Returns:
            Formatted dataset summary
        """
        summary_parts = [
            "Dataset Characteristics:",
            f"- Rows: {profile_result.row_count:,}",
            f"- Columns: {profile_result.column_count}",
            f"- Quality Score: {profile_result.quality_score}/100",
            "",
            "Column Types:",
        ]

        # Add column type breakdown
        type_breakdown = self._format_column_types(profile_result.column_profiles)
        summary_parts.append(type_breakdown)

        return "\n".join(summary_parts)

    def _create_issues_summary(self, profile_result: Any) -> str:
        """Create summary of detected issues.

        Args:
            profile_result: Profiling results

        Returns:
            Formatted issues summary
        """
        issues = []

        # High null percentage
        high_null_cols = [
            p.column_name
            for p in profile_result.column_profiles
            if p.null_percentage > 30
        ]
        if high_null_cols:
            issues.append(
                f"- High null percentage (>30%) in: {', '.join(high_null_cols[:5])}"
            )
            if len(high_null_cols) > 5:
                issues.append(f"  ... and {len(high_null_cols) - 5} more columns")

        # Duplicates
        if hasattr(profile_result, "quality_metrics"):
            dup_pct = profile_result.quality_metrics.duplicate_percentage
            if dup_pct > 5:
                issues.append(f"- {dup_pct:.1f}% duplicate rows detected")

        # Outliers
        outlier_cols = []
        for p in profile_result.column_profiles:
            if hasattr(p, "outliers") and p.outliers:
                outlier_pct = p.outliers.get("percentage", 0)
                if outlier_pct > 10:
                    outlier_cols.append(p.column_name)

        if outlier_cols:
            issues.append(
                f"- Outliers detected (>10%) in: {', '.join(outlier_cols[:5])}"
            )
            if len(outlier_cols) > 5:
                issues.append(f"  ... and {len(outlier_cols) - 5} more columns")

        # High correlation
        if hasattr(profile_result, "quality_metrics"):
            corr_matrix = profile_result.quality_metrics.correlation_matrix
            if corr_matrix:
                high_corr_pairs = []
                for col1, correlations in corr_matrix.items():
                    for col2, corr_value in correlations.items():
                        if abs(corr_value) > 0.9:
                            high_corr_pairs.append(f"{col1} & {col2}")
                            if len(high_corr_pairs) >= 3:
                                break
                    if len(high_corr_pairs) >= 3:
                        break

                if high_corr_pairs:
                    issues.append(
                        f"- High correlation (>0.9) between: {', '.join(high_corr_pairs)}"
                    )

        return "\n".join(issues) if issues else "No major issues detected"

    def _format_column_types(self, column_profiles: list[Any]) -> str:
        """Format column types for prompt.

        Args:
            column_profiles: List of column profiles

        Returns:
            Formatted column type breakdown
        """
        type_counts: dict[str, int] = {}
        for profile in column_profiles:
            dtype = profile.data_type
            type_counts[dtype] = type_counts.get(dtype, 0) + 1

        lines = []
        for dtype, count in sorted(type_counts.items()):
            lines.append(f"- {dtype}: {count} column(s)")

        return "\n".join(lines)

    def _load_templates(self) -> dict[str, str]:
        """Load prompt templates from files.

        Returns:
            Dictionary of template name to template content
        """
        templates = {}
        template_dir = Path(__file__).parent / "templates"

        template_files = {
            "ml": "ml_prompt.txt",
            "business": "business_prompt.txt",
            "anomaly": "anomaly_prompt.txt",
            "general": "general_prompt.txt",
        }

        for key, filename in template_files.items():
            template_path = template_dir / filename
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    templates[key] = f.read()
                logger.debug(f"Loaded template: {key}")
            except FileNotFoundError:
                logger.warning(f"Template file not found: {template_path}")
                # Fallback to basic template
                templates[key] = self._get_fallback_template()

        return templates

    def _get_fallback_template(self) -> str:
        """Get fallback template if file loading fails.

        Returns:
            Basic template string
        """
        return """
You are a data quality expert analyzing a dataset.

{dataset_summary}

Detected Issues:
{issues_summary}

Please provide insights in this format:
CRITICAL: [issue] | RECOMMENDATION: [action]
WARNING: [issue] | RECOMMENDATION: [action]
INFO: [insight]
"""
