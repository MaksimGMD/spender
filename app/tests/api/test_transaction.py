from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.category import create_random_category
from app.tests.utils.account import create_random_account


def test_create_transaction(client: TestClient, db: Session, user_token_headers: dict):
    category = create_random_category(db=db)
    account = create_random_account(db=db)
    data = {
        "amount": 50.0,
        "description": "Test Transaction",
        "category_id": category.id,
        "account_id": account.id,
    }

    response = client.post("/transaction/", headers=user_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()

    assert Decimal(content["amount"]) == Decimal(data["amount"])
    assert content["description"] == data["description"]
    assert content["category_id"] == data["category_id"]
    assert content["account_id"] == data["account_id"]
    assert "date" in content
    
def test_get_account_transactions(client: TestClient, db: Session, user_token_headers: dict):
    account = create_random_account(db=db)

    response = client.get(f"/transaction/account_transactions/{account.id}", headers=user_token_headers)

    assert response.status_code == 200
    
    

