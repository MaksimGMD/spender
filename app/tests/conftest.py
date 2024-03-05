import pytest
from typing import Generator, Dict, Annotated

from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from app.db.database import engine
from app.main import app

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
