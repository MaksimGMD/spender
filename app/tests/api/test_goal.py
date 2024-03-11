from decimal import Decimal

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.tests.utils.goal import create_random_goal


def test_create_goal(client: TestClient, user_token_headers: dict):
    data = {
        "name": "Новая цель",
        "amount": 100,
        "target_amount": 10000,
    }
    response = client.post("/goal/", headers=user_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    
    assert content["name"] == data["name"]
    assert Decimal(content["amount"]) == Decimal(data["amount"])
    assert Decimal(content["target_amount"]) == Decimal(data["target_amount"])
    assert "deadline" in content
    assert "id" in content
    assert "user_id" in content
    assert "is_achieved" in content


def test_get_goal(client: TestClient, user_token_headers: dict, db: Session):
    goal = create_random_goal(db=db)
    response = client.get(f"/goal/{goal.id}", headers=user_token_headers)
    assert response.status_code == 200
    content = response.json()
    
    assert content["name"] == goal.name
    assert Decimal(content["amount"]) == Decimal(goal.amount)
    assert Decimal(content["target_amount"]) == Decimal(goal.target_amount)
    assert content["user_id"] == goal.user_id
    assert "deadline" in content


def test_update_goal(client: TestClient, user_token_headers: dict, db: Session):
    goal = create_random_goal(db=db)
    data = {
        "name": "Изменённая цель",
        "amount": 300.5,
        "target_amount": 700.50,
    }
    response = client.put(
        f"/goal/{goal.id}", headers=user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert Decimal(content["amount"]) == Decimal(data["amount"])
    assert Decimal(content["target_amount"]) == Decimal(data["target_amount"])
    assert "id" in content
    assert "user_id" in content


def test_delete_goal(client: TestClient, user_token_headers: dict, db: Session):
    goal = create_random_goal(db=db)
    response = client.delete(f"/goal/{goal.id}", headers=user_token_headers)
    assert response.status_code == 200
    content = response.text
    assert f"Цель: {goal.name} удалена" in content


def test_update_goal_forbidden(
    client: TestClient, user_token_headers: dict, db: Session
):
    other_user_goal = create_random_goal(db=db, user_id=999)

    data = {
        "name": "Изменённая цель",
        "amount": 300.5,
        "target_amount": 700.50,
    }
    response = client.put(
        f"/goal/{other_user_goal.id}",
        headers=user_token_headers,
        json=data,
    )

    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Пользователь не может изменить не свою цель"

def test_add_accumulated_amount(client: TestClient, user_token_headers: dict, db: Session):
    goal = create_random_goal(db=db)

    data = {"amount": 50.0}

    response = client.put(
        f"/goal/add_accumulated_amount/{goal.id}",
        headers=user_token_headers,
        json=data,
    )

    assert response.status_code == 200

    content = response.json()
    assert content["name"] == goal.name
    assert Decimal(content["amount"]) == Decimal(goal.amount)
    assert Decimal(content["target_amount"]) == Decimal(goal.target_amount)
    assert content["user_id"] == goal.user_id
    assert "deadline" in content
    assert "id" in content
    assert "is_achieved" in content