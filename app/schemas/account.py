from typing import Optional
from enum import Enum

from pydantic import BaseModel, condecimal


class CurrencyEnum(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"
    GBP = "GBP"
    AUD = "AUD"


class AccountBase(BaseModel):
    name: Optional[str] = None
    balance: Optional[condecimal(max_digits=10, decimal_places=2)] = 0.0
    currency: Optional[CurrencyEnum] = CurrencyEnum.RUB
    type: Optional[str] = None
    is_active: Optional[bool] = True


class AccountCreate(AccountBase):
    user_id: int


class AccountUpdate(AccountBase):
    pass


class AccountSchema(AccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
