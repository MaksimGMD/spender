from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    region: str = "RU"
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
