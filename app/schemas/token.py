from typing import Union
from pydantic import BaseModel
from fastapi.param_functions import Form


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Содержимое JWT Token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None


class OAuth2PasswordRequestForm:
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
    ):
        self.username = username
        self.password = password
