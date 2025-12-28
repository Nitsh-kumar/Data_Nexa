"""Custom exception classes."""

from typing import Any


class AppException(Exception):
    """Base application exception.
    
    Attributes:
        status_code: HTTP status code
        detail: Error message
        error_code: Application-specific error code
    """

    def __init__(
        self, status_code: int, detail: str, error_code: str | None = None
    ) -> None:
        """Initialize exception.
        
        Args:
            status_code: HTTP status code
            detail: Error message
            error_code: Application-specific error code
        """
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        super().__init__(detail)


class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(self, detail: str = "Resource not found") -> None:
        """Initialize exception.
        
        Args:
            detail: Error message
        """
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND")


class UnauthorizedException(AppException):
    """Unauthorized access exception."""

    def __init__(self, detail: str = "Unauthorized") -> None:
        """Initialize exception.
        
        Args:
            detail: Error message
        """
        super().__init__(status_code=401, detail=detail, error_code="UNAUTHORIZED")


class ValidationException(AppException):
    """Validation error exception."""

    def __init__(self, detail: str = "Validation error") -> None:
        """Initialize exception.
        
        Args:
            detail: Error message
        """
        super().__init__(status_code=422, detail=detail, error_code="VALIDATION_ERROR")


class AIServiceException(AppException):
    """AI service operation failed."""

    def __init__(self, detail: str = "AI service error") -> None:
        """Initialize exception.
        
        Args:
            detail: Error message
        """
        super().__init__(status_code=500, detail=detail, error_code="AI_SERVICE_ERROR")


class ClaudeAPIException(AppException):
    """Claude API call failed."""

    def __init__(self, detail: str = "Claude API error") -> None:
        """Initialize exception.
        
        Args:
            detail: Error message
        """
        super().__init__(status_code=503, detail=detail, error_code="CLAUDE_API_ERROR")
