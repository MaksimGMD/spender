import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from faker import Faker
from app.tests.conftest import SessionDep

from app.schemas.user import UserCreate
from app import crud

fake = Faker()


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    auth = client.post("auth/access-token", data=data)
    response = auth.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: SessionDep) -> UserCreate:
    user_in = UserCreate(
        name=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        password="".join(random.choices(string.ascii_letters + string.digits, k=12)),
    )

    user = crud.user.create(db=db, obj_in=user_in)
    return user
