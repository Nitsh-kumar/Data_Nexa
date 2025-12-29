"""AI service for generating insights and recommendations."""

import hashlib
import logging
from typing import Any

from app.core.ai_engine.cache_manager import CacheManager
from app.core.ai_engine.groq_client import GroqAPIException, GroqClient
from app.core.ai_engine.code_generator import CodeGenerator
from app.core.ai_engine.insight_categorizer import InsightCategorizer
from app.core.ai_engine.models import CategorizedInsight
from app.core.ai_engine.prompt_builder import PromptBuilder
from app.core.ai_engine.response_parser import ResponseParser
from app.core.ai_engine.story_generator import StoryGenerator

logger = logging.getLogger(__name__)


class AIServiceException(Exception):
    """AI service operation failed."""

    pass


class AIService:
    """Main AI service for generating insights."""

    def __init__(
        self,
        groq_client: GroqClient | None = None,
        prompt_builder: PromptBuilder | None = None,
        response_parser: ResponseParser | None = None,
        insight_categorizer: InsightCategorizer | None = None,
        code_generator: CodeGenerator | None = None,
        story_generator: StoryGenerator | None = None,
        cache_manager: CacheManager | None = None,
    ):
        """Initialize AI service.

        Args:
            groq_client: Groq API client
            prompt_builder: Prompt builder
            response_parser: Response parser
            insight_categorizer: Insight categorizer
            code_generator: Code generator
            story_generator: Story generator
            cache_manager: Cache manager
        """
        self.groq = groq_client or GroqClient()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.parser = response_parser or ResponseParser()
        self.categorizer = insight_categorizer or InsightCategorizer()
        self.code_generator = code_generator or CodeGenerator()
        self.story_generator = story_generator or StoryGenerator()
        self.cache = cache_manager or CacheManager()

        logger.info("AIService initialized with all components")

    async def generate_insights(
        self,
        analysis_id: int,
        profile_result: Any,
        goal_type: str,
    ) -> list[CategorizedInsight]:
        """Generate AI-powered insights from profiling results.
        
        This is the main entry point for the AI insights generation workflow.
        It orchestrates all components to transform raw profiling data into
        actionable insights with code snippets and executive summaries.
        
        WORKFLOW:
        1. Check Redis cache for existing insights (24-hour TTL)
        2. Build context-aware prompt based on goal type
        3. Call Claude API with retry logic
        4. Parse and validate response
        5. Categorize insights by type and priority
        6. Generate Python code snippets for fixes
        7. Create executive summary in plain English
        8. Cache results for future requests
        
        FALLBACK STRATEGY:
        If Claude API fails at any step, automatically falls back to
        rule-based insights to ensure users always get results.

        Args:
            analysis_id: Analysis record ID (used for caching)
            profile_result: Complete profiling results with column stats
            goal_type: User's analysis goal (ml_preparation, business_reporting, etc.)

        Returns:
            List of categorized insights sorted by priority

        Raises:
            AIServiceException: If insight generation fails completely
        """
        try:
            logger.info(
                f"Generating insights for analysis {analysis_id} with goal '{goal_type}'"
            )

            # STEP 1: Check cache first to reduce API costs (~80% hit rate)
            # Cache key is based on analysis characteristics (rows, columns, quality score)
            cache_key = self._generate_cache_key(analysis_id, profile_result)
            cached_insights = await self.cache.get(cache_key)

            if cached_insights:
                logger.info(f"Cache HIT - Using cached insights for analysis {analysis_id}")
                # Convert cached dict back to CategorizedInsight objects
                return [CategorizedInsight(**i) for i in cached_insights]

            logger.info(f"Cache MISS - Generating new insights")

            # STEP 2: Build context-aware prompt
            # Selects appropriate template based on goal_type
            # Includes dataset summary, detected issues, and anonymized sample data
            prompt = await self.prompt_builder.build(
                profile_result=profile_result,
                goal_type=goal_type,
            )

            logger.info(f"Built prompt with {len(prompt)} characters")

            # STEP 3: Call Groq API with automatic retry logic
            # Retries 3 times with exponential backoff (2s, 4s, 8s)
            # Handles rate limits and timeouts gracefully
            try:
                response = await self.groq.generate(prompt=prompt)
                logger.info(f"Received Groq response with {len(response)} characters")

            except GroqAPIException as e:
                # If API fails after retries, use rule-based fallback
                logger.warning(f"Groq API failed: {str(e)}, using fallback")
                return await self._generate_fallback_insights(profile_result, goal_type)

            # STEP 4: Validate response format
            # Ensures response contains expected severity keywords (CRITICAL, WARNING, INFO)
            if not self.parser.validate_response(response):
                logger.warning("Invalid Groq response format, using fallback")
                return await self._generate_fallback_insights(profile_result, goal_type)

            # STEP 5: Parse response into structured insights
            # Expected format: "SEVERITY: description | RECOMMENDATION: action"
            raw_insights = await self.parser.parse(response)
            logger.info(f"Parsed {len(raw_insights)} raw insights")

            if not raw_insights:
                logger.warning("No insights parsed from response, using fallback")
                return await self._generate_fallback_insights(profile_result, goal_type)

            # STEP 6: Categorize and prioritize insights
            # - Detects insight type (missing_data, duplicates, outliers, etc.)
            # - Calculates priority (1-5, lower is higher priority)
            # - Determines impact level (High/Medium/Low)
            # - Extracts affected column names from description
            categorized_insights = await self.categorizer.categorize(
                raw_insights,
                profile_result,
                goal_type,
            )

            logger.info(f"Categorized {len(categorized_insights)} insights")

            # STEP 7: Generate code snippets for critical and warning insights
            # Creates Python code using pandas operations to fix identified issues
            # Only generates code for actionable insights (not informational)
            for insight in categorized_insights:
                if insight.recommendation and insight.severity in {"critical", "warning"}:
                    try:
                        code = await self.code_generator.generate(
                            insight=insight,
                            language="python",  # Can also generate SQL or R
                        )
                        insight.code_suggestion = code
                    except Exception as e:
                        logger.warning(f"Failed to generate code: {str(e)}")
                        insight.code_suggestion = None

            # STEP 8: Generate executive summary
            # Creates plain English summary for non-technical users
            # Includes dataset description, quality assessment, and top issues
            try:
                summary = await self.story_generator.generate(
                    profile_result=profile_result,
                    insights=categorized_insights,
                )

                # Add summary as first insight with highest priority (0)
                # This ensures it appears at the top of the insights list
                summary_insight = CategorizedInsight(
                    severity="info",
                    type="quality_issue",
                    description=summary,
                    recommendation="",
                    priority=0,  # Highest priority to show first
                    affected_columns=[],
                    impact="Low",
                    code_suggestion=None,
                )

                categorized_insights.insert(0, summary_insight)

            except Exception as e:
                logger.warning(f"Failed to generate summary: {str(e)}")

            # STEP 9: Cache results for 24 hours
            # Reduces API costs and improves response time for repeated requests
            try:
                await self.cache.set(cache_key, categorized_insights)
                logger.info(f"Cached insights for analysis {analysis_id}")
            except Exception as e:
                # Cache failure is non-critical, log and continue
                logger.warning(f"Failed to cache insights: {str(e)}")

            logger.info(
                f"Successfully generated {len(categorized_insights)} insights "
                f"for analysis {analysis_id}"
            )

            return categorized_insights

        except Exception as e:
            logger.error(f"Failed to generate insights: {str(e)}", exc_info=True)
            raise AIServiceException(f"Failed to generate insights: {str(e)}")

    async def _generate_fallback_insights(
        self,
        profile_result: Any,
        goal_type: str,
    ) -> list[CategorizedInsight]:
        """Generate rule-based insights when AI is unavailable.

        Args:
            profile_result: Profiling results
            goal_type: User's analysis goal

        Returns:
            List of fallback insights
        """
        logger.info("Generating fallback rule-based insights")

        insights = []

        # Critical: High null percentage
        for col_profile in profile_result.column_profiles:
            if col_profile.null_percentage > 50:
                insights.append(
                    CategorizedInsight(
                        severity="critical",
                        type="missing_data",
                        description=f"Column '{col_profile.column_name}' has {col_profile.null_percentage:.1f}% missing values",
                        recommendation="Consider dropping this column or investigating the cause of missing data",
                        priority=1,
                        affected_columns=[col_profile.column_name],
                        impact="High",
                        code_suggestion=None,
                    )
                )

        # Warning: High duplicates
        if hasattr(profile_result, "quality_metrics"):
            dup_pct = profile_result.quality_metrics.duplicate_percentage
            if dup_pct > 5:
                insights.append(
                    CategorizedInsight(
                        severity="warning",
                        type="duplicates",
                        description=f"Dataset contains {dup_pct:.1f}% duplicate rows",
                        recommendation="Remove duplicate rows to improve data quality",
                        priority=2,
                        affected_columns=[],
                        impact="High",
                        code_suggestion=None,
                    )
                )

        # Warning: Outliers
        for col_profile in profile_result.column_profiles:
            if hasattr(col_profile, "outliers") and col_profile.outliers:
                outlier_pct = col_profile.outliers.get("percentage", 0)
                if outlier_pct > 10:
                    insights.append(
                        CategorizedInsight(
                            severity="warning",
                            type="outliers",
                            description=f"Column '{col_profile.column_name}' has {outlier_pct:.1f}% outliers",
                            recommendation="Review outliers to determine if they are errors or valid extreme values",
                            priority=2,
                            affected_columns=[col_profile.column_name],
                            impact="Medium",
                            code_suggestion=None,
                        )
                    )

        # Info: Quality summary
        quality_score = profile_result.quality_score
        if quality_score >= 85:
            insights.append(
                CategorizedInsight(
                    severity="info",
                    type="quality_issue",
                    description=f"Data quality is good ({quality_score}/100). The dataset is ready for analysis.",
                    recommendation="",
                    priority=5,
                    affected_columns=[],
                    impact="Low",
                    code_suggestion=None,
                )
            )
        elif quality_score < 70:
            insights.append(
                CategorizedInsight(
                    severity="warning",
                    type="quality_issue",
                    description=f"Data quality is below average ({quality_score}/100). Address the issues before analysis.",
                    recommendation="Review and fix the critical and warning issues identified",
                    priority=2,
                    affected_columns=[],
                    impact="High",
                    code_suggestion=None,
                )
            )

        # Generate code for insights
        for insight in insights:
            if insight.recommendation and insight.severity in {"critical", "warning"}:
                try:
                    code = await self.code_generator.generate(
                        insight=insight,
                        language="python",
                    )
                    insight.code_suggestion = code
                except Exception as e:
                    logger.warning(f"Failed to generate fallback code: {str(e)}")

        logger.info(f"Generated {len(insights)} fallback insights")

        return insights

    def _generate_cache_key(
        self,
        analysis_id: int,
        profile_result: Any,
    ) -> str:
        """Generate cache key based on analysis characteristics.

        Args:
            analysis_id: Analysis ID
            profile_result: Profiling results

        Returns:
            Cache key
        """
        # Use hash of key characteristics
        key_data = (
            f"{analysis_id}_"
            f"{profile_result.row_count}_"
            f"{profile_result.column_count}_"
            f"{profile_result.quality_score}"
        )
        return hashlib.md5(key_data.encode()).hexdigest()

    def get_token_stats(self) -> dict[str, Any]:
        """Get token usage statistics.

        Returns:
            Dictionary with token usage stats
        """
        return self.groq.get_token_stats()

    async def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        return await self.cache.get_stats()
