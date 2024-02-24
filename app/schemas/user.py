from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    region: Optional[str] = "RU"
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True
