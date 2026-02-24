"""Configuration for CA Biositing Web Service.

This module provides API-specific configuration using Pydantic Settings.
"""

from __future__ import annotations

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class WebServiceConfig(BaseSettings):
    """Configuration for the web service.

    Attributes:
        api_title: Title for the API
        api_description: Description for the API
        api_version: Version of the API
        cors_origins: List of allowed CORS origins
        cors_allow_credentials: Whether to allow credentials in CORS
        cors_allow_methods: Allowed HTTP methods for CORS
        cors_allow_headers: Allowed headers for CORS
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="API_",
    )

    api_title: str = "CA Biositing API"
    api_description: str = "REST API for CA Biositing bioeconomy data"
    api_version: str = "0.1.0"

    # CORS configuration
    cors_origins: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Alternative frontend port
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # JWT authentication configuration
    # Override API_JWT_SECRET_KEY in production via GCP Secret Manager
    jwt_secret_key: str = "changeme-not-for-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    jwt_cookie_secure: bool = True


# Global configuration instance
config = WebServiceConfig()
