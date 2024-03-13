from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from faker import Faker

from app.tests.utils.user import create_random_user
fake = Faker()


def test_create_user(client: TestClient, user_token_headers: dict):
    user_data = {
        "name": "New User",
        "email": "newuser@example.com",
        "phone_number": fake.phone_number(),
        "password": "newpassword",
        "region": "RU",
    }

    response = client.post("/user/", headers=user_token_headers, json=user_data)
    assert response.status_code == 200

    content = response.json()
    assert content["name"] == user_data["name"]
    assert content["phone_number"] == user_data["phone_number"]
    assert content["email"] == user_data["email"]
    assert content["region"] == user_data["region"]
    assert "id" in content


def test_get_users(client: TestClient, db: Session, user_token_headers: dict):
    create_random_user(db=db)
    create_random_user(db=db)

    response = client.get("/user/", headers=user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 2


def test_delete_user(client: TestClient, user_token_headers: dict, db: Session):
    user = create_random_user(db=db)
    response = client.delete(f"/user/{user.id}", headers=user_token_headers)
    assert response.status_code == 200
    content = response.text
    assert f"Пользователь: {user.name} удалён" in content
