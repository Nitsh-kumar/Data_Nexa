"""Application configuration using Pydantic Settings."""

from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="allow"
    )

    # Project
    PROJECT_NAME: str = "DataInsight Pro Backend"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database
    POSTGRES_SERVER: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str | None = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: Any) -> str:
        """Build database URL from components.
        
        Args:
            v: Existing database URL if provided
            info: Validation info containing other field values
            
        Returns:
            Complete database URL
        """
        if isinstance(v, str):
            return v
        # Build PostgreSQL URL if components are provided
        if all([
            info.data.get("POSTGRES_USER"),
            info.data.get("POSTGRES_PASSWORD"),
            info.data.get("POSTGRES_SERVER"),
            info.data.get("POSTGRES_DB"),
        ]):
            return str(
                PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=info.data.get("POSTGRES_USER"),
                    password=info.data.get("POSTGRES_PASSWORD"),
                    host=info.data.get("POSTGRES_SERVER"),
                    port=info.data.get("POSTGRES_PORT"),
                    path=info.data.get("POSTGRES_DB"),
                )
            )
        # Default to SQLite if no DATABASE_URL provided
        return "sqlite+aiosqlite:///./datainsight.db"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list[str] = [".csv", ".xlsx", ".xls"]

    # AI / Claude API
    CLAUDE_API_KEY: str
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS: int = 2000
    CLAUDE_TEMPERATURE: float = 0.7

    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    CACHE_TTL: int = 86400  # 24 hours
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False


settings = Settings()
