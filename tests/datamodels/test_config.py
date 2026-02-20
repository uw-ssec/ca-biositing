"""Tests for Settings.database_url construction modes."""

from ca_biositing.datamodels.config import Settings


def test_database_url_explicit(monkeypatch):
    """Explicit DATABASE_URL takes highest priority."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/mydb")
    monkeypatch.delenv("INSTANCE_CONNECTION_NAME", raising=False)
    settings = Settings()
    assert settings.database_url == "postgresql://user:pass@host:5432/mydb"


def test_database_url_unix_socket(monkeypatch):
    """INSTANCE_CONNECTION_NAME produces a Unix socket URL for Cloud Run."""
    # Set DATABASE_URL to empty string so it overrides the .env file value (falsy)
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.setenv("INSTANCE_CONNECTION_NAME", "my-project:us-west1:my-instance")
    monkeypatch.setenv("DB_USER", "appuser")
    monkeypatch.setenv("DB_PASS", "secret")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    settings = Settings()
    assert settings.database_url == (
        "postgresql://appuser:secret@/mydb"
        "?host=/cloudsql/my-project:us-west1:my-instance"
    )


def test_database_url_tcp_fallback(monkeypatch):
    """Falls back to TCP format when no overrides are set."""
    # Set DATABASE_URL to empty string so it overrides the .env file value (falsy)
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.setenv("INSTANCE_CONNECTION_NAME", "")
    monkeypatch.setenv("POSTGRES_USER", "pguser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "pgpass")
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    settings = Settings()
    assert settings.database_url == "postgresql://pguser:pgpass@localhost:5432/mydb"
