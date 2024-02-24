from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

from app import crud
from app.api.deps import get_current_user, get_session, CurrentUser
from app.schemas.user import UserCreate, UserSchema, UserUpdate
from app.models.user import User

router = APIRouter()


@router.get(
    "/", dependencies=[Depends(get_current_user)], response_model=List[UserSchema]
)
def get_users(session: Session = Depends(get_session)):
    """
    **Получение списка пользователей.**

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.

    Returns:
        List[UserSchema]: Список объектов с данными пользователей.
    """
    users = session.exec(select(User)).all()
    return users


@router.post("/", response_model=UserSchema)
def create_user(*, session: Session = Depends(get_session), user_in: UserCreate):
    """
    **Создание нового пользователя.**

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.
        user_in (UserCreate): Объект с данными нового пользователя.

    Returns:
        UserSchema: Объект с данными созданного пользователя.

    Raises:
        HTTPException: В случае, если пользователь с таким email уже существует, возникает исключение с кодом HTTP 400 Bad Request.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с такой почтой уже существует",
        )

    user = crud.user.create(db=session, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUser,
    user_id: int,
    user_in: UserUpdate,
):
    """
    **Обновление данных пользователя.**

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.
        current_user (CurrentUser): Объект текущего авторизованного пользователя. Получается через зависимость.
        user_id (int): Уникальный идентификатор пользователя, данные которого нужно обновить.
        user_in (UserUpdate): Объект с обновленными данными пользователя.

    Returns:
        UserSchema: Объект с данными обновленного пользователя.

    Raises:
        HTTPException: В случае, если пользователь не найден или текущий пользователь пытается изменить другого пользователя,
                       возникает исключение с кодом HTTP 404 Not Found или HTTP 400 Bad Request.
    """
    user = crud.user.get(session, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )
    if user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не может изменять другого пользователя",
        )

    user = crud.user.update(session, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}")
def delete_user(
    *, session: Session = Depends(get_session), current_user: CurrentUser, user_id: int
):
    """
    **Удаление пользователя.**

    Args:
        session (Session, optional): Экземпляр сессии базы данных. Получается через зависимость.
        current_user (CurrentUser): Объект текущего авторизованного пользователя. Получается через зависимость.
        user_id (int): Уникальный идентификатор пользователя, которого нужно удалить.

    Returns:
        str: Сообщение об успешном удалении пользователя.

    Raises:
        HTTPException: В случае, если пользователь не найден или текущий пользователь пытается удалить себя,
                       возникает исключение с кодом HTTP 404 Not Found или HTTP 400 Bad Request.
    """
    user = crud.user.get(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может удалить себя"
        )

    crud.user.remove(session, id=user_id)
    return f"Пользователь {user.name} удалён"
