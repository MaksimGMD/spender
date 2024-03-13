from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.auth import get_user_by_email


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


def test_get_me(client: TestClient, user_token_headers: dict, db: Session):
    user = get_user_by_email(session=db, email=settings.EMAIL_TEST_USER)
    response = client.get("/auth/me", headers=user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == user.name
    assert content["email"] == user.email
    assert content["phone_number"] == user.phone_number
    assert content["region"] == user.region
