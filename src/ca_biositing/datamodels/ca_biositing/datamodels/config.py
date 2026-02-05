from pathlib import Path
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Determine the project root (directory containing "pixi.toml") to locate the shared .env file.
# Determine the project root (directory containing "pixi.toml") to locate the shared .env file.
_project_root = Path(__file__).resolve().parent
while not (_project_root / "pixi.toml").exists():
    _project_root = _project_root.parent
_env_path = _project_root / "resources" / "docker" / ".env"


class Settings(BaseSettings):
    """
    Application settings and configuration for the datamodels package.

    Uses Pydantic Settings to load configuration from environment variables
    and .env files.
    """
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "biositing"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=str(_env_path),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    @property
    def database_url(self) -> str:
        """Constructs the database URL from components if not explicitly set."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
