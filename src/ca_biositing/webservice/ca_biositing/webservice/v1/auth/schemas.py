"""Pydantic schemas for authentication request/response payloads."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Decoded JWT token data."""

    username: Optional[str] = None


class UserCreate(BaseModel):
    """Payload for creating a new API user."""

    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: bool = False


class UserResponse(BaseModel):
    """Public representation of an API user (no password hash)."""

    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: bool
    disabled: bool
