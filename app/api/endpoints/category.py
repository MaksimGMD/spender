from typing import List

from fastapi import APIRouter, Depends, HTTPException
from app.models.category import Category
from app.schemas.category import CategorySchema, CategoryCreate, CategoryUpdate
from app.api.deps import get_current_user, CurrentUser, SessionDep
from app import crud

router = APIRouter()

NOT_FOUND_MESSAGE = "Категория не найдена"


@router.get("/{id}", response_model=CategorySchema)
def get_category(*, session: SessionDep, current_user: CurrentUser, id: int):
    """
    **Получает информацию о категории по её id.**

    Args:
        session (SessionDep): Сессия базы данных.
        current_user (CurrentUser): Текущий авторизованный пользователь.
        id (int): Идентификатор категории.

    Returns:
        CategorySchema: Информация о категории.

    Raises:
        HTTPException: Если категория не найдена или если пользователь пытается получить категорию не своего пользователя.
    """
    category = crud.category.get(session, id)

    if not category:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    if category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return category


@router.get("/", response_model=List[CategorySchema])
def get_categories(*, session: SessionDep, current_user: CurrentUser):
    """
    **Получает список категорий для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.

    Returns:
        List[CategorySchema]: Список категорий пользователя.
    """
    categories = (
        session.query(Category).where(Category.user_id == current_user.id).all()
    )
    return categories


@router.post(
    "/", response_model=CategorySchema
)
def create_category(
    *, session: SessionDep, category_in: CategoryCreate, current_user: CurrentUser
):
    """
    **Создает новую категорию для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        category_in (CategoryCreate): Данные для создания новой категории.

    Returns:
        CategorySchema: Созданная категория.
    """
    category = crud.category.create(db=session, obj_in=category_in, user_id=current_user.id)
    return category


@router.put("/{category_id}", response_model=CategorySchema)
def update_category(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    category_id: int,
    category_in: CategoryUpdate,
):
    """
    **Обновляет существующую категорию для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        category_id (int): Идентификатор обновляемой категории.
        category_in (CategoryUpdate): Данные для обновления категории.

    Returns:
        CategorySchema: Обновленная категория.

    Raises:
        HTTPException: Если категория не найдена или пользователь пытается изменить чужую категорию.
    """
    category = crud.category.get(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может изменить не свою категорию"
        )

    category = crud.category.update(session, db_obj=category, obj_in=category_in)
    return category


@router.delete("/{category_id}")
def delete_category(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    category_id: int,
):
    """
    **Удаляет категорию для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        category_id (int): Идентификатор удаляемой категории.

    Returns:
        str: Сообщение об удалении категории.

    Raises:
        HTTPException: Если категория не найдена или пользователь пытается удалить чужую категорию.
    """
    category = crud.category.get(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может удалить не свою категорию"
        )

    crud.category.remove(session, id=category_id)
    return f"Категория: {category.name} удалена"
