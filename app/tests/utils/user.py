import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from faker import Faker
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app import crud
from app.core.config import settings
from app.models import User

fake = Faker()


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    """
    Получение заголовков аутентификации для тестов.

    Args:
        client (TestClient): Экземпляр тестового клиента.
        email (str): Электронная почта пользователя.
        password (str): Пароль пользователя.

    Returns:
        Dict[str, str]: Заголовки аутентификации.
    """
    data = {"username": email, "password": password}

    auth = client.post("auth/access-token", data=data)
    response = auth.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    """
    Создание случайного пользователя в базе данных для тестов.

    Args:
        db (Session): Экземпляр сессии базы данных.

    Returns:
        UserCreate: Данные созданного пользователя.
    """
    user_in = UserCreate(
        name=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        password="".join(random.choices(string.ascii_letters + string.digits, k=12)),
    )

    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_email(*, client: TestClient, email: str, db: Session):
    """
    Получение аутентификационных заголовков для тестов по электронной почте.

    Args:
        client (TestClient): Экземпляр тестового клиента.
        email (str): Электронная почта пользователя.
        db (Session): Экземпляр сессии базы данных.

    Returns:
        Dict[str, str]: Заголовки аутентификации.
    """
    user = crud.auth.get_user_by_email(session=db, email=email)
    if not user:
        user_in = UserCreate(
            name="admin",
            email=email,
            phone_number=fake.phone_number(),
            password=settings.PASSWORD_TEST_USER,
        )

        crud.user.create(db=db, obj_in=user_in)

    return user_authentication_headers(
        client=client, email=email, password=settings.PASSWORD_TEST_USER
    )
