from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.category import create_random_category


def test_create_category(client: TestClient, user_token_headers: dict):
    data = {"name": "Продукты", "color": "red", "icon_name": "product_icon"}
    response = client.post(
        "/category/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["color"] == data["color"]
    assert content["icon_name"] == data["icon_name"]
    assert "id" in content
    assert "user_id" in content


def test_get_category(client: TestClient, user_token_headers: dict, db: Session):
    category = create_random_category(db=db)
    response = client.get(f"/category/{category.id}", headers=user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == category.name
    assert content["color"] == category.color
    assert content["icon_name"] == category.icon_name
    assert content["user_id"] == category.user_id


def test_update_category(client: TestClient, user_token_headers: dict, db: Session):
    category = create_random_category(db=db)
    data = {"name": "Новая категория", "color": "blue", "icon_name": "updated_icon"}
    response = client.put(
        f"/category/{category.id}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["color"] == data["color"]
    assert content["icon_name"] == data["icon_name"]
    assert "id" in content
    assert "user_id" in content


def test_delete_category(client: TestClient, user_token_headers: dict, db: Session):
    category = create_random_category(db=db)
    response = client.delete(f"/category/{category.id}", headers=user_token_headers)
    assert response.status_code == 200
    content = response.text
    assert f"Категория: {category.name} удалена" in content


def test_update_category_forbidden(
    client: TestClient, user_token_headers: dict, db: Session
):
    other_user_category = create_random_category(db=db, user_id=999)

    data = {"name": "Updated Name", "color": "green", "icon_name": "updated_icon"}
    response = client.put(
        f"/category/{other_user_category.id}",
        headers=user_token_headers,
        json=data,
    )

    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Пользователь не может изменить не свою категорию"
