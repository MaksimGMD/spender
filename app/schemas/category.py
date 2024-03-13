from typing import Optional

from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    icon_name: Optional[str] = None
    
class CategoryCreate(CategoryBase):
    pass
    
class CategoryUpdate(CategoryBase):
    pass


class CategorySchema(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True