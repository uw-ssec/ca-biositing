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
    resp = httpx.post(
        f"{base_url}/v1/auth/token",
        data={"username": username, "password": password},
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def client(base_url, auth_headers):
    with httpx.Client(base_url=base_url, headers=auth_headers) as c:
        yield c
