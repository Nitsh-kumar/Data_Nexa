"""Logging configuration for the application."""

import logging
import sys
from pathlib import Path

from app.config import settings


def setup_logging() -> None:
    """Set up logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler
            logging.FileHandler(log_dir / "app.log"),
        ],
    )

    # Set specific log levels for different modules
    logging.getLogger("app.core.ai_engine").setLevel(logging.INFO)
    logging.getLogger("app.api").setLevel(logging.INFO)
    logging.getLogger("app.services").setLevel(logging.INFO)

    # Reduce noise from third-party libraries
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logging.info("Logging configured successfully")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
