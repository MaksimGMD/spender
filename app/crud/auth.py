from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select
from fastapi import Depends

from app.models.user import User
from app.core.security import verify_password

from app.api.deps import get_session


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    Получает пользователя из базы данных по адресу электронной почты.

    Args:
        session (Session): Экземпляр сессии базы данных.
        email (str): Адрес электронной почты пользователя.

    Returns:
        User | None: Возвращает экземпляр пользователя если найден, в противном случае None.
    """
    statement = select(User).where(func.lower(User.email) == func.lower(email))
    session_user = session.exec(statement).first()
    return session_user


def authenticate(
    *, session: Session = Depends(get_session), email: str, password: str
) -> User | None:
    """
    Проверяет учетные данные пользователя и выполняет аутентификацию.

    Args:
        session (Session, optional): Экземпляр сессии базы данных.
        email (str): Адрес электронной почты пользователя.
        password (str): Пароль пользователя.

    Returns:
        User | None: Возвращает экземпляр пользователя, если аутентификация успешна, в противном случае None.
    """
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
