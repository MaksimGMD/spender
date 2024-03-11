import pytest, os
from typing import Generator, Dict

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings
from app.api.deps import get_session

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def test_app() -> Generator:
    Base.metadata.create_all(engine)
    _app = app
    yield _app
    Base.metadata.drop_all(engine)
    os.remove("test.db")


@pytest.fixture(scope="session")
def db() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    
    yield db
    
    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(test_app, db: Session) -> Generator:
    def get_test_db_session():
        try:
            yield db
        finally:
            pass

    test_app.dependency_overrides[get_session] = get_test_db_session
    with TestClient(test_app) as client:
        yield client
        test_app.dependency_overrides = {}


@pytest.fixture(scope="module")
def user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
