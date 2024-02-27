from typing import Optional
from datetime import datetime
from pydantic import BaseModel, condecimal


class TransactionBase(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = 0.0
    date: Optional[datetime] = None
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    category_id: int
    account_id: int


class TransactionUpdate(TransactionBase):
    pass


class TransactionSchema(TransactionBase):
    id: int
    category_id: int
    account_id: int

    class Config:
        from_attributes = True


class TransactionsOut(TransactionSchema):
    account_name: str
    category_name: str
    
class TransactionTransferCreate(TransactionBase):
    account_id: int
    to_account_id: int
    category_id: Optional[int] = None