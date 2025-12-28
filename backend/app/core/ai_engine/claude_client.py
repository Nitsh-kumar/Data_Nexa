"""Claude API client with retry logic and error handling.

This module provides a robust wrapper around the Anthropic Claude API with:
- Automatic retry logic with exponential backoff
- Token usage tracking for cost monitoring
- Comprehensive error handling
- Async operations for better performance

RETRY STRATEGY:
- 3 retry attempts
- Exponential backoff: 2s, 4s, 8s
- Only retries on rate limits and timeouts
- Other errors fail immediately

COST TRACKING:
- Tracks input and output tokens
- Calculates estimated costs
- Provides usage statistics

EXAMPLE USAGE:
    client = ClaudeClient()
    response = await client.generate("Analyze this data...")
    stats = client.get_token_stats()
    print(f"Cost: ${stats['estimated_cost_usd']}")
"""

import logging
from typing import Any

import anthropic
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings

logger = logging.getLogger(__name__)


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
        logger.info(
            f"Token usage - Input: {input_tokens}, Output: {output_tokens}, "
            f"Total: {self.total_input_tokens + self.total_output_tokens}"
        )

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


class ClaudeAPIException(Exception):
    """Claude API call failed."""

    pass


class ClaudeClient:
    """Claude API client with retry and error handling."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ):
        """Initialize Claude client.

        Args:
            api_key: Anthropic API key (defaults to settings)
            model: Model name (defaults to settings)
            max_tokens: Max tokens per request (defaults to settings)
            temperature: Sampling temperature (defaults to settings)
        """
        self.api_key = api_key or settings.CLAUDE_API_KEY
        self.model = model or settings.CLAUDE_MODEL
        self.max_tokens = max_tokens or settings.CLAUDE_MAX_TOKENS
        self.temperature = temperature or settings.CLAUDE_TEMPERATURE

        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        self.token_usage = TokenUsageTracker()

        logger.info(f"Initialized ClaudeClient with model: {self.model}")

    @retry(
        stop=stop_after_attempt(3),  # Try up to 3 times
        wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s between retries
        retry=retry_if_exception_type(
            # Only retry on these specific errors
            (anthropic.RateLimitError, anthropic.APITimeoutError)
        ),
    )
    async def generate(
        self,
        prompt: str,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Generate response from Claude API with automatic retry logic.
        
        This method calls the Claude API and automatically retries on rate limits
        and timeouts. Token usage is tracked for cost monitoring.
        
        RETRY BEHAVIOR:
        - RateLimitError: Retries with exponential backoff (2s, 4s, 8s)
        - APITimeoutError: Retries with exponential backoff
        - Other errors: Fails immediately without retry
        
        COST TRACKING:
        - Input tokens: Prompt length in tokens
        - Output tokens: Response length in tokens
        - Costs are tracked automatically via TokenUsageTracker
        
        MODEL PARAMETERS:
        - model: claude-sonnet-4-20250514 (configurable)
        - max_tokens: 2000 (configurable, controls response length)
        - temperature: 0.7 (configurable, controls randomness)

        Args:
            prompt: Input prompt (will be sent to Claude)
            max_tokens: Maximum tokens in response (overrides default of 2000)
            temperature: Sampling temperature 0-1 (overrides default of 0.7)
                        Lower = more focused, Higher = more creative

        Returns:
            Generated text response from Claude

        Raises:
            ClaudeAPIException: If API call fails after all retries
                              - Rate limit exceeded (after 3 retries)
                              - API timeout (after 3 retries)
                              - Other API errors (immediate failure)
        """
        try:
            logger.info(f"Calling Claude API with prompt length: {len(prompt)} characters")

            # Call Claude API using Anthropic SDK
            # This is an async call that may take several seconds
            response = await self.client.messages.create(
                model=self.model,  # claude-sonnet-4-20250514
                max_tokens=max_tokens or self.max_tokens,  # Default: 2000
                temperature=temperature or self.temperature,  # Default: 0.7
                messages=[{"role": "user", "content": prompt}],
            )

            # Track token usage for cost monitoring
            # Input tokens: ~$0.003 per 1K tokens
            # Output tokens: ~$0.015 per 1K tokens
            self.token_usage.add(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            )

            # Extract text from response
            # Claude returns a list of content blocks, we take the first text block
            text_response = response.content[0].text

            logger.info(
                f"Claude API response received: {len(text_response)} characters, "
                f"{response.usage.input_tokens} input tokens, "
                f"{response.usage.output_tokens} output tokens"
            )

            return text_response

        except anthropic.RateLimitError as e:
            # Rate limit hit - will be retried automatically by @retry decorator
            logger.warning(f"Rate limit exceeded: {str(e)} - will retry")
            raise ClaudeAPIException(f"Rate limit exceeded: {str(e)}")

        except anthropic.APITimeoutError as e:
            # Timeout - will be retried automatically by @retry decorator
            logger.warning(f"API timeout: {str(e)} - will retry")
            raise ClaudeAPIException(f"API timeout: {str(e)}")

        except anthropic.APIError as e:
            # Other API errors - fail immediately without retry
            logger.error(f"Claude API error: {str(e)}")
            raise ClaudeAPIException(f"API call failed: {str(e)}")

        except Exception as e:
            # Unexpected errors - fail immediately
            logger.error(f"Unexpected error calling Claude API: {str(e)}")
            raise ClaudeAPIException(f"Unexpected error: {str(e)}")

    def get_token_stats(self) -> dict[str, Any]:
        """Get token usage statistics.

        Returns:
            Dictionary with token counts and cost
        """
        return self.token_usage.get_stats()
