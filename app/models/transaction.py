from datetime import datetime

from sqlalchemy import BigInteger, String, Column, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


# Модель транзакции пользователя
class Transaction(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    date = Column(DateTime, index=True, nullable=False, default=datetime.utcnow)
    description = Column(String, nullable=True)

    category_id = Column(
        BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    category = relationship("Category", back_populates="transactions")
    
    account_id = Column(
        BigInteger, ForeignKey("account.id", ondelete="CASCADE"), nullable=False
    )
    account = relationship("Account", back_populates="transactions")
