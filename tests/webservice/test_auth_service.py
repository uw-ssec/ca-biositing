"""Unit tests for the auth service module.

Tests password hashing, JWT creation/decoding, and user authentication logic
in isolation (no HTTP layer).
"""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from ca_biositing.datamodels.models import ApiUser
from ca_biositing.webservice.services.auth_service import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

SECRET = "test-secret-key-must-be-32-chars-!"
ALGORITHM = "HS256"


# --- Password hashing ---


def test_get_password_hash_returns_argon2_hash():
    h = get_password_hash("mypassword")
    assert h.startswith("$argon2"), f"Expected Argon2 hash, got: {h[:20]}"


def test_verify_password_correct():
    h = get_password_hash("mypassword")
    assert verify_password("mypassword", h) is True


def test_verify_password_incorrect():
    h = get_password_hash("mypassword")
    assert verify_password("wrongpass", h) is False


# --- JWT creation ---


def test_create_access_token_contains_sub_and_exp():
    import jwt as pyjwt

    token = create_access_token({"sub": "alice"}, SECRET, ALGORITHM)
    payload = pyjwt.decode(token, SECRET, algorithms=[ALGORITHM])
    assert payload["sub"] == "alice"
    assert "exp" in payload


def test_create_access_token_custom_expiry():
    import jwt as pyjwt
    from datetime import datetime, timezone

    before = datetime.now(timezone.utc)
    token = create_access_token({"sub": "bob"}, SECRET, ALGORITHM, timedelta(minutes=5))
    payload = pyjwt.decode(token, SECRET, algorithms=[ALGORITHM])
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    # Expiry should be ~5 minutes from now (allow 10s slack)
    diff = (exp - before).total_seconds()
    assert 290 <= diff <= 310, f"Expected ~300s expiry, got {diff}s"


# --- JWT decoding ---


def test_decode_access_token_valid():
    token = create_access_token({"sub": "alice"}, SECRET, ALGORITHM)
    username = decode_access_token(token, SECRET, ALGORITHM)
    assert username == "alice"


def test_decode_access_token_expired():
    token = create_access_token({"sub": "alice"}, SECRET, ALGORITHM, timedelta(seconds=-1))
    result = decode_access_token(token, SECRET, ALGORITHM)
    assert result is None


def test_decode_access_token_invalid_token():
    result = decode_access_token("not.a.valid.token", SECRET, ALGORITHM)
    assert result is None


def test_decode_access_token_wrong_secret():
    token = create_access_token({"sub": "alice"}, SECRET, ALGORITHM)
    result = decode_access_token(token, "wrong-secret-key-must-be-32-chars", ALGORITHM)
    assert result is None


def test_decode_access_token_missing_sub():
    import jwt as pyjwt
    from datetime import datetime, timedelta, timezone

    # Encode a token with no 'sub' claim
    payload = {"exp": datetime.now(timezone.utc) + timedelta(minutes=5)}
    token = pyjwt.encode(payload, SECRET, algorithm=ALGORITHM)
    result = decode_access_token(token, SECRET, ALGORITHM)
    assert result is None


# --- authenticate_user ---


def _make_mock_session(user: ApiUser | None):
    """Return a mock SQLModel Session whose exec().first() returns user."""
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.first.return_value = user
    mock_session.exec.return_value = mock_result
    return mock_session


def test_authenticate_user_success():
    hashed = get_password_hash("correctpass")
    user = ApiUser(
        id=1,
        username="alice",
        hashed_password=hashed,
        is_admin=False,
        disabled=False,
    )
    session = _make_mock_session(user)
    result = authenticate_user(session, "alice", "correctpass")
    assert result is user


def test_authenticate_user_wrong_password():
    hashed = get_password_hash("correctpass")
    user = ApiUser(
        id=1,
        username="alice",
        hashed_password=hashed,
        is_admin=False,
        disabled=False,
    )
    session = _make_mock_session(user)
    result = authenticate_user(session, "alice", "wrongpass")
    assert result is None


def test_authenticate_user_nonexistent():
    session = _make_mock_session(None)
    result = authenticate_user(session, "nobody", "anypass")
    assert result is None


def test_authenticate_user_disabled():
    hashed = get_password_hash("correctpass")
    user = ApiUser(id=1, username="dis", hashed_password=hashed, is_admin=False, disabled=True)
    result = authenticate_user(_make_mock_session(user), "dis", "correctpass")
    assert result is None
