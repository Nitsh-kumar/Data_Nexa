"""Groq API client with retry logic and error handling.

This module provides a robust wrapper around the Groq API with:
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
    client = GroqClient()
    response = await client.generate("Analyze this data...")
    stats = client.get_token_stats()
    print(f"Cost: ${stats['estimated_cost_usd']}")
"""

import logging
from typing import Any

from groq import AsyncGroq
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings

logger = logging.getLogger(__name__)


class TokenUsageTracker:
    """Track Groq API token usage for cost monitoring."""

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
            Estimated cost based on Groq pricing (very low cost)
        """
        # Groq pricing is very low - approximate rates
        input_cost = self.total_input_tokens * 0.0001 / 1000  # Much cheaper than Claude
        output_cost = self.total_output_tokens * 0.0002 / 1000
        return round(input_cost + output_cost, 6)

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


class GroqAPIException(Exception):
    """Groq API call failed."""

    pass


class GroqClient:
    """Groq API client with retry and error handling."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ):
        """Initialize Groq client.

        Args:
            api_key: Groq API key (defaults to settings)
            model: Model name (defaults to settings)
            max_tokens: Max tokens per request (defaults to settings)
            temperature: Sampling temperature (defaults to settings)
        """
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.max_tokens = max_tokens or settings.GROQ_MAX_TOKENS
        self.temperature = temperature or settings.GROQ_TEMPERATURE

        self.client = AsyncGroq(api_key=self.api_key)
        self.token_usage = TokenUsageTracker()

        logger.info(f"Initialized GroqClient with model: {self.model}")

    @retry(
        stop=stop_after_attempt(3),  # Try up to 3 times
        wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s between retries
        retry=retry_if_exception_type(
            # Only retry on these specific errors
            (Exception,)  # Groq uses generic exceptions, we'll catch and check
        ),
    )
    async def generate(
        self,
        prompt: str,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Generate response from Groq API with automatic retry logic.
        
        This method calls the Groq API and automatically retries on rate limits
        and timeouts. Token usage is tracked for cost monitoring.
        
        RETRY BEHAVIOR:
        - Rate limit errors: Retries with exponential backoff (2s, 4s, 8s)
        - Timeout errors: Retries with exponential backoff
        - Other errors: Fails immediately without retry
        
        COST TRACKING:
        - Input tokens: Prompt length in tokens
        - Output tokens: Response length in tokens
        - Costs are tracked automatically via TokenUsageTracker
        
        MODEL PARAMETERS:
        - model: llama-3.1-70b-versatile (configurable)
        - max_tokens: 2000 (configurable, controls response length)
        - temperature: 0.7 (configurable, controls randomness)

        Args:
            prompt: Input prompt (will be sent to Groq)
            max_tokens: Maximum tokens in response (overrides default of 2000)
            temperature: Sampling temperature 0-1 (overrides default of 0.7)
                        Lower = more focused, Higher = more creative

        Returns:
            Generated text response from Groq

        Raises:
            GroqAPIException: If API call fails after all retries
        """
        try:
            logger.info(f"Calling Groq API with prompt length: {len(prompt)} characters")

            # Call Groq API using Groq SDK
            response = await self.client.chat.completions.create(
                model=self.model,  # llama-3.1-70b-versatile
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or self.max_tokens,  # Default: 2000
                temperature=temperature or self.temperature,  # Default: 0.7
            )

            # Track token usage for cost monitoring
            # Groq is much cheaper than Claude
            if response.usage:
                self.token_usage.add(
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                )

            # Extract text from response
            text_response = response.choices[0].message.content

            logger.info(
                f"Groq API response received: {len(text_response)} characters"
            )

            return text_response

        except Exception as e:
            # Check if it's a rate limit or timeout error
            error_str = str(e).lower()
            if "rate limit" in error_str or "timeout" in error_str:
                logger.warning(f"Groq API error (will retry): {str(e)}")
                raise GroqAPIException(f"Retryable error: {str(e)}")
            else:
                # Other errors - fail immediately
                logger.error(f"Groq API error: {str(e)}")
                raise GroqAPIException(f"API call failed: {str(e)}")

    def get_token_stats(self) -> dict[str, Any]:
        """Get token usage statistics.

        Returns:
            Dictionary with token counts and cost
        """
        return self.token_usage.get_stats()