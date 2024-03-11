from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient):
    login_data = {
        "username": settings.EMAIL_TEST_USER,
        "password": settings.PASSWORD_TEST_USER,
    }
    auth = client.post("/auth/access-token", data=login_data)
    tokens = auth.json()
    assert auth.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
