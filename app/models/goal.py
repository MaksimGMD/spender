from sqlalchemy import (
    BigInteger,
    String,
    Column,
    ForeignKey,
    DateTime,
    Numeric,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


# Модель целей
class Goal(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    target_amount = Column(Numeric(precision=10, scale=2), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False, default=0.0)
    deadline = Column(DateTime, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    is_achieved = Column(Boolean, default=False)

    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="goals")
