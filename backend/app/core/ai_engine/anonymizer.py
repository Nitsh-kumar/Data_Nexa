"""Data anonymization for sensitive information before sending to Claude API."""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class DataAnonymizer:
    """Anonymize sensitive data for API calls."""

    async def anonymize(self, column_profiles: list[Any]) -> str:
        """Anonymize column profiles for sample data.

        Args:
            column_profiles: Column profiles to anonymize

        Returns:
            Anonymized sample data as JSON string
        """
        anonymized = []

        for profile in column_profiles:
            col_data = {
                "name": profile.column_name,
                "type": profile.data_type,
            }

            # Anonymize based on semantic type
            if profile.semantic_type == "email":
                col_data["sample"] = "user***@domain.com"
                col_data["note"] = "Email addresses detected"

            elif profile.semantic_type == "phone":
                col_data["sample"] = "***-***-1234"
                col_data["note"] = "Phone numbers detected"

            elif profile.semantic_type == "identifier":
                col_data["sample"] = "ID_***"
                col_data["note"] = "Unique identifiers detected"

            elif profile.data_type == "numeric":
                stats = profile.statistics
                if stats:
                    min_val = stats.get("min", 0)
                    max_val = stats.get("max", 0)
                    col_data["sample"] = f"Range: {min_val} - {max_val}"
                    col_data["note"] = f"Numeric values"
                else:
                    col_data["sample"] = "[numeric data]"

            elif profile.data_type == "categorical":
                stats = profile.statistics
                if stats and "top_values" in stats:
                    # Show top 3 categories without actual values
                    top_count = min(3, len(stats["top_values"]))
                    col_data["sample"] = f"{top_count} categories"
                    col_data["note"] = f"{stats.get('unique_count', 0)} unique values"
                else:
                    col_data["sample"] = "[categorical data]"

            elif profile.data_type == "datetime":
                stats = profile.statistics
                if stats:
                    col_data["sample"] = f"Date range: {stats.get('min_date', 'N/A')} to {stats.get('max_date', 'N/A')}"
                    col_data["note"] = "Temporal data"
                else:
                    col_data["sample"] = "[datetime data]"

            elif profile.data_type == "text":
                stats = profile.statistics
                if stats:
                    avg_len = stats.get("avg_length", 0)
                    col_data["sample"] = f"Text (avg length: {avg_len} chars)"
                    col_data["note"] = "Text data"
                else:
                    col_data["sample"] = "[text data]"

            else:
                col_data["sample"] = "[anonymized]"

            # Add null information
            col_data["null_percentage"] = round(profile.null_percentage, 2)

            anonymized.append(col_data)

        logger.info(f"Anonymized {len(anonymized)} columns")

        return json.dumps(anonymized, indent=2)

    def anonymize_value(self, value: str, data_type: str) -> str:
        """Anonymize a single value based on its type.

        Args:
            value: Value to anonymize
            data_type: Type of the value

        Returns:
            Anonymized value
        """
        if data_type == "email":
            # Keep domain, mask username
            if "@" in value:
                parts = value.split("@")
                return f"{parts[0][:2]}***@{parts[1]}"
            return "***@domain.com"

        elif data_type == "phone":
            # Keep last 4 digits
            digits = "".join(c for c in value if c.isdigit())
            if len(digits) >= 4:
                return f"***-***-{digits[-4:]}"
            return "***-***-****"

        elif data_type == "identifier":
            # Replace with generic ID
            return "ID_***"

        else:
            # Generic anonymization
            return "***"
