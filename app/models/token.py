from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Содержимое JWT Token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None
