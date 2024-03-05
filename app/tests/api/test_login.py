from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    auth = client.post("auth/access-token", data=login_data)
    tokens = auth.json()
    assert auth.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    auth = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = auth.json()
    assert auth.status_code == 200
    assert "email" in result
