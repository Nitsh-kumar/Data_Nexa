"""Response parser for Claude API responses."""

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RawInsight:
    """Parsed insight from Claude response."""

    severity: str
    description: str
    recommendation: str


class ResponseParser:
    """Parse Claude API responses into structured insights."""

    async def parse(self, response: str) -> list[RawInsight]:
        """Parse Claude response into insights.

        Args:
            response: Raw text response from Claude

        Returns:
            List of parsed insights
        """
        insights = []
        lines = response.strip().split("\n")

        logger.info(f"Parsing response with {len(lines)} lines")

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Parse format: "SEVERITY: description | RECOMMENDATION: action"
            if ":" in line:
                try:
                    insight = self._parse_line(line)
                    if insight:
                        insights.append(insight)
                        logger.debug(
                            f"Parsed insight: {insight.severity} - {insight.description[:50]}..."
                        )
                except Exception as e:
                    logger.warning(f"Failed to parse line {line_num}: {line[:100]} - {str(e)}")
                    continue

        logger.info(f"Successfully parsed {len(insights)} insights")

        return insights

    def _parse_line(self, line: str) -> RawInsight | None:
        """Parse a single line into an insight.

        Args:
            line: Line to parse

        Returns:
            Parsed insight or None if parsing fails
        """
        # Check if line contains recommendation separator
        if "|" in line:
            # Format: "SEVERITY: description | RECOMMENDATION: action"
            parts = line.split("|", 1)
            severity_part = parts[0].strip()
            rec_part = parts[1].strip() if len(parts) > 1 else ""

            # Extract severity and description
            severity_match = re.match(
                r"(CRITICAL|WARNING|INFO):\s*(.+)", severity_part, re.IGNORECASE
            )
            if not severity_match:
                return None

            severity = severity_match.group(1).lower()
            description = severity_match.group(2).strip()

            # Extract recommendation
            recommendation = ""
            if rec_part:
                rec_match = re.match(r"RECOMMENDATION:\s*(.+)", rec_part, re.IGNORECASE)
                if rec_match:
                    recommendation = rec_match.group(1).strip()
                else:
                    # If no RECOMMENDATION: prefix, use the whole part
                    recommendation = rec_part

            return RawInsight(
                severity=severity,
                description=description,
                recommendation=recommendation,
            )

        else:
            # Format without recommendation: "SEVERITY: description"
            severity_match = re.match(
                r"(CRITICAL|WARNING|INFO):\s*(.+)", line, re.IGNORECASE
            )
            if severity_match:
                severity = severity_match.group(1).lower()
                description = severity_match.group(2).strip()

                return RawInsight(
                    severity=severity,
                    description=description,
                    recommendation="",
                )

        return None

    def validate_response(self, response: str) -> bool:
        """Validate that response has expected format.

        Args:
            response: Response to validate

        Returns:
            True if response appears valid
        """
        if not response or len(response.strip()) < 10:
            return False

        # Check if response contains at least one severity keyword
        severity_keywords = ["CRITICAL:", "WARNING:", "INFO:"]
        return any(keyword in response.upper() for keyword in severity_keywords)
