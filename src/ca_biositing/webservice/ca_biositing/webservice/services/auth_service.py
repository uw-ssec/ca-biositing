"""Authentication service for JWT-based user authentication.

Provides password hashing, JWT creation/decoding, and user authentication logic.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from pwdlib import PasswordHash
from sqlmodel import Session, select

from ca_biositing.datamodels.models import ApiUser

logger = logging.getLogger(__name__)

# Argon2 password hasher
password_hash = PasswordHash.recommended()

# Pre-computed dummy hash for constant-time comparison on missing users
DUMMY_HASH = password_hash.hash("dummy-password-for-timing-safety")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against an Argon2 hash."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using Argon2."""
    return password_hash.hash(password)


def authenticate_user(session: Session, username: str, password: str) -> Optional[ApiUser]:
    """Look up a user by username and verify their password.

    Uses a constant-time dummy hash check for non-existent users to prevent
    timing-based username enumeration.

    Returns the ApiUser on success, or None on failure (wrong password,
    nonexistent user, or disabled account).
    """
    user = session.exec(select(ApiUser).where(ApiUser.username == username)).first()
    if not user:
        # Constant-time dummy check to prevent username enumeration
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if user.disabled:
        return None
    return user


def create_access_token(
    data: dict,
    secret_key: str,
    algorithm: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload data to encode (must include "sub" claim).
        secret_key: The HMAC signing secret.
        algorithm: JWT signing algorithm (e.g. "HS256").
        expires_delta: Token lifetime; defaults to 30 minutes.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(
    token: str,
    secret_key: str,
    algorithm: str,
) -> Optional[str]:
    """Decode a JWT access token and return the username (sub claim).

    Returns None if the token is invalid, expired, or missing the sub claim.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: Optional[str] = payload.get("sub")
        return username
    except jwt.InvalidTokenError:
        return None
