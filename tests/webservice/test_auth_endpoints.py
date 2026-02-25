"""Integration tests for auth API endpoints.

Tests the full HTTP layer: login, register, refresh, logout, and that
feedstocks routes correctly require a valid JWT.

The test client uses an in-memory SQLite DB with only the api_user table.
Feedstocks endpoints will return 404/500 (no data), but authentication
decisions happen before DB queries, so 401 vs non-401 is what we check.
"""

from __future__ import annotations

import pytest

# conftest.py provides: auth_client, auth_session, admin_user, regular_user,
#                        disabled_user, admin_token, user_token


# --- Login ---


def test_login_success(auth_client, admin_user):
    resp = auth_client.post(
        "/v1/auth/token",
        data={"username": "admin", "password": "adminpass"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    # HTTP-only cookie must be set
    assert "access_token" in resp.cookies


def test_login_wrong_password(auth_client, admin_user):
    resp = auth_client.post(
        "/v1/auth/token",
        data={"username": "admin", "password": "wrongpass"},
    )
    assert resp.status_code == 401


def test_login_nonexistent_user(auth_client):
    resp = auth_client.post(
        "/v1/auth/token",
        data={"username": "nobody", "password": "anypass"},
    )
    assert resp.status_code == 401


# --- Protected endpoint ---


def test_protected_endpoint_no_token(auth_client):
    resp = auth_client.get("/v1/feedstocks/analysis/resources/1/geoid/06001/parameters")
    assert resp.status_code == 401


def test_protected_endpoint_with_bearer(auth_client, admin_token):
    resp = auth_client.get(
        "/v1/feedstocks/analysis/resources/1/geoid/06001/parameters",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    # Auth passes — endpoint may return 404/500 due to no real DB data, but NOT 401
    assert resp.status_code != 401


def test_protected_endpoint_with_cookie(auth_client, admin_token):
    """Cookie-based auth should work without Authorization header."""
    resp = auth_client.get(
        "/v1/feedstocks/analysis/resources/1/geoid/06001/parameters",
        cookies={"access_token": admin_token},
    )
    assert resp.status_code != 401


def test_protected_endpoint_invalid_token(auth_client):
    resp = auth_client.get(
        "/v1/feedstocks/analysis/resources/1/geoid/06001/parameters",
        headers={"Authorization": "Bearer this.is.invalid"},
    )
    assert resp.status_code == 401


# --- Register ---


def test_register_as_admin(auth_client, admin_token):
    resp = auth_client.post(
        "/v1/auth/register",
        json={
            "username": "newuser",
            "password": "newpass123",
            "email": "new@test.com",
            "is_admin": False,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["username"] == "newuser"
    assert "hashed_password" not in body


def test_register_as_non_admin(auth_client, user_token):
    resp = auth_client.post(
        "/v1/auth/register",
        json={"username": "anotheruser", "password": "pass123"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


def test_register_no_token(auth_client):
    resp = auth_client.post(
        "/v1/auth/register",
        json={"username": "anotheruser", "password": "pass123"},
    )
    assert resp.status_code == 401


def test_register_duplicate_username(auth_client, admin_token, admin_user):
    # admin user already exists
    resp = auth_client.post(
        "/v1/auth/register",
        json={"username": "admin", "password": "anypassword"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 409


# --- Refresh ---


def test_refresh_valid_token(auth_client, admin_token):
    resp = auth_client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert "access_token" in resp.cookies


def test_refresh_no_token(auth_client):
    resp = auth_client.post("/v1/auth/refresh")
    assert resp.status_code == 401


# --- Logout ---


def test_logout_clears_cookie(auth_client, admin_token):
    resp = auth_client.post(
        "/v1/auth/logout",
        cookies={"access_token": admin_token},
    )
    assert resp.status_code == 200
    assert resp.json() == {"message": "Logged out"}
    # The cookie should be deleted (max-age=0 or absent in cookies after logout)
    # TestClient reflects Set-Cookie with empty value + max-age=0
    set_cookie_header = resp.headers.get("set-cookie", "")
    assert "access_token" in set_cookie_header
    assert "Max-Age=0" in set_cookie_header or "max-age=0" in set_cookie_header


# --- Disabled user ---


def test_disabled_user_rejected(auth_client, disabled_user):
    resp = auth_client.post(
        "/v1/auth/token",
        data={"username": "disabled", "password": "disabledpass"},
    )
    assert resp.status_code == 401
