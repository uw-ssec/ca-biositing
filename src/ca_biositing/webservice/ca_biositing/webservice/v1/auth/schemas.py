"""Pydantic schemas for authentication request/response payloads."""

from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Token(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str


class UserCreate(BaseModel):
    """Payload for creating a new API user."""

    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    email: Optional[str] = Field(default=None, max_length=254)
    full_name: Optional[str] = None
    is_admin: bool = False

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Invalid email address")
        return v


class UserResponse(BaseModel):
    """Public representation of an API user (no password hash)."""

    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: bool
    disabled: bool
