from typing import Optional
from datetime import datetime
from pydantic import BaseModel, condecimal


class BudgetPeriod(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class BudgetBase(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = 0.0
    period: BudgetPeriod = BudgetPeriod.week
    start_date: Optional[datetime] = None
    description: Optional[str] = None


class BudgetCreate(BudgetBase):
    user_id: int
    category_id: int


class BudgetUpdate(BudgetBase):
    pass


class BudgetSchema(BudgetBase):
    id: int
    user_id: int
    category_id: int

    class Config:
        from_attributes = True
