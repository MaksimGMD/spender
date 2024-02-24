from sqlalchemy import BigInteger, String, Column
from sqlalchemy.orm import relationship

from app.models.base import Base


# Модель пользователя
class User(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    region = Column(String(2), nullable=False, default="RU")

    categories = relationship("Category", back_populates="user", cascade="all,delete", uselist=True)