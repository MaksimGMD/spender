from sqlalchemy import BigInteger, String, Column
from sqlalchemy.orm import validates
from pydantic import EmailStr

from app.models.base import Base


# Модель пользователя
class User(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    region = Column(String(2), nullable=False, default="RU")
