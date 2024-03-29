from sqlalchemy import BigInteger, String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base


# Модель категорий расходов
class Category(Base):
    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    name = Column(String, index=True, nullable=False)
    color = Column(String, nullable=True)
    icon_name = Column(String, nullable=True)

    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="categories")

    transactions = relationship(
        "Transaction", back_populates="category", cascade="all,delete", uselist=True
    )

    budgets = relationship(
        "Budget", back_populates="category", cascade="all,delete", uselist=True
    )
