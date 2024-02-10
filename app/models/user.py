from sqlalchemy import BigInteger, String, Column
from sqlalchemy.orm import validates
from pydantic import EmailStr, validator
from passlib.hash import bcrypt

from app.db.base_class import Base


# Модель пользователя
class User(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    region = Column(String(2), nullable=False, default="RU")

    # Валидация email
    @validates("email")
    def validate_email(cls, key, email):
        return EmailStr()(email)

    # Хэширует пароль при его установке
    @validator("hashed_password", pre=True, always=True)
    def hash_password(cls, v):
        return bcrypt.hash(v)
