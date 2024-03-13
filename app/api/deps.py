from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.database import engine, SessionLocal
from app.models import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
    
SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    session: SessionDep, token: TokenDep
) -> User:
    """
    Получает текущего пользователя на основе переданного токена аутентификации.

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.
        token (str, optional): Токен аутентификации пользователя. Получается через зависимость.

    Returns:
        User: Экземпляр пользователя, если аутентификация успешна.

    Raises:
        HTTPException: В случае неудачной аутентификации, возникает исключение с кодом HTTP 403 Forbidden или 404 Not Found.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не удалось подтвердить права доступа",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
