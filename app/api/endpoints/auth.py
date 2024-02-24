from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.api.deps import get_session, CurrentUser
from app.core.security import create_access_token
from app.crud.auth import authenticate
from app.schemas.token import Token, OAuth2PasswordRequestForm
from app.schemas.user import UserSchema


router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    **Аутентификация пользователя и выдача токена доступа.**

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.
        form_data (OAuth2PasswordRequestForm): Данные формы для запроса токена (логин и пароль).

    Returns:
        Token: Объект токена доступа.

    Raises:
        HTTPException: В случае неудачной аутентификации, возникает исключение с кодом HTTP 400 Bad Request.
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя или пароль")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/access-token")
def login_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    **Аутентификация пользователя и выдача токена доступа (вариант для использования в заголовке Authorization).**

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.
        form_data (OAuth2PasswordRequestForm): Данные формы для запроса токена (логин и пароль).

    Returns:
        Token: Объект токена доступа.

    Raises:
        HTTPException: В случае неудачной аутентификации, возникает исключение с кодом HTTP 400 Bad Request.
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_expires)
    )


@router.get("/me", response_model=UserSchema)
def get_me(current_user: CurrentUser):
    """
    **Получение данных текущего авторизованного пользователя.**

    Args:
        current_user (CurrentUser): Объект текущего авторизованного пользователя. Получается через зависимость.

    Returns:
        UserSchema: Объект с данными пользователя.
    """
    return current_user
