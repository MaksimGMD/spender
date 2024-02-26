from sqlalchemy import BigInteger, String, Column, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


# Модель счёта пользователя
class Account(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    balance = Column(Numeric(precision=10, scale=2), nullable=False)
    currency = Column(String, nullable=True, default="RUB")
    type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="accounts")

    transactions = relationship(
        "Transaction", back_populates="account", cascade="all,delete", uselist=True
    )