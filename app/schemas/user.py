from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str | None = None
    region: str = "RU"
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
