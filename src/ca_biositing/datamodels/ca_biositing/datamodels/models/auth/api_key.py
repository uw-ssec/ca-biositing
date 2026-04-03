"""ApiKey model for per-client API key authentication."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class ApiKey(SQLModel, table=True):
    """Per-client API key for authenticating external callers.

    Raw keys are shown exactly once at creation and never stored. Only the
    Argon2 hash is persisted. The key_prefix (first 8 chars of the raw key)
    is stored in plaintext to allow efficient lookup before hash verification.

    Rate limiting uses a DB-based sliding window with SELECT FOR UPDATE to
    handle multiple Cloud Run instances without requiring Redis.
    """

    __tablename__ = "api_key"

    id: Optional[int] = Field(default=None, primary_key=True)
    api_user_id: int = Field(foreign_key="api_user.id", nullable=False, index=True)
    name: str = Field(nullable=False)
    key_prefix: str = Field(nullable=False, index=True)
    key_hash: str = Field(nullable=False, unique=True)
    is_active: bool = Field(default=True, nullable=False)
    rate_limit_per_minute: int = Field(default=60, nullable=False)
    rate_window_start: Optional[datetime] = Field(default=None)
    rate_window_count: int = Field(default=0, nullable=False)
    last_used_at: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")},
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": sa.text("CURRENT_TIMESTAMP"),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
