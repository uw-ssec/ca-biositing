import os

import httpx
import pytest


@pytest.fixture(scope="module")
def base_url() -> str:
    return os.getenv("CA_BIOSITING_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="module")
def auth_headers(base_url) -> dict:
    username = os.getenv("CA_BIOSITING_TEST_USERNAME")
    password = os.getenv("CA_BIOSITING_TEST_PASSWORD")
    if not username or not password:
        pytest.skip(
            "CA_BIOSITING_TEST_USERNAME and CA_BIOSITING_TEST_PASSWORD "
            "environment variables are required for integration tests"
        )
    try:
        resp = httpx.post(
            f"{base_url}/v1/auth/token",
            data={"username": username, "password": password},
        )
        resp.raise_for_status()
    except httpx.ConnectError:
        pytest.skip(f"Could not connect to {base_url} — is the server running?")
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def client(base_url, auth_headers):
    with httpx.Client(base_url=base_url, headers=auth_headers) as c:
        yield c
