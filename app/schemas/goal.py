from typing import Optional
from datetime import datetime
from pydantic import BaseModel, condecimal


class GoalBase(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[condecimal(max_digits=10, decimal_places=2)] = 0.0
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = 0.0
    deadline: Optional[datetime] = None


class GoalCreate(GoalBase):
    user_id: int


class GoalUpdate(GoalBase):
    pass

class GoalUpdateAmount(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = 0.0


class GoalSchema(GoalBase):
    id: int
    user_id: int
    is_achieved: bool

    class Config:
        from_attributes = True
