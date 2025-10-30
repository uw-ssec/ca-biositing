"""Configuration for CA Biositing data models.

This module provides configuration management for database models using Pydantic Settings.
"""

from __future__ import annotations

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    """Configuration for database models.
    
    Attributes:
        database_url: PostgreSQL database connection URL
        echo_sql: Whether to echo SQL statements (for debugging)
        pool_size: Database connection pool size
        max_overflow: Maximum number of connections that can be created beyond pool_size
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    database_url: str = "postgresql://user:password@localhost:5432/ca_biositing"
    echo_sql: bool = False
    pool_size: int = 5
    max_overflow: int = 10


# Global configuration instance
config = ModelConfig()
