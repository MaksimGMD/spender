from datetime import datetime

from sqlalchemy import Column, BigInteger, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

# Модель бюджета
class Budget(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    period = Column(String, nullable=False, default="week")  # Значения 'day', 'week', 'month', 'year'
    start_date = Column(DateTime, index=True, nullable=False, default=datetime.utcnow)
    description = Column(String, nullable=True)
    
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="budgets")

    category_id = Column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="budgets")