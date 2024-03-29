from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.account import Account
from app.schemas.account import (
    AccountSchema,
    AccountCreate,
    AccountUpdate,
    AccountTransactions,
)
from app.api.deps import SessionDep, get_current_user, CurrentUser
from app import crud

router = APIRouter()

NOT_FOUND_MESSAGE = "Счёт не найден"


@router.get("/{id}", response_model=AccountSchema)
def get_account(*, session: SessionDep, current_user: CurrentUser, id: int):
    """
    **Получает информацию о счёте по его id.**

    Args:
        session (SessionDep): Сессия базы данных.
        current_user (CurrentUser): Текущий авторизованный пользователь.
        id (int): Идентификатор счёта.

    Returns:
        List[AccountSchema]: Информация о счёте.

    Raises:
        HTTPException: Если счёт не найден или если пользователь пытается получить счёт не своего пользователя.
    """
    account = crud.account.get(session, id)

    if not account:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return account


@router.get("/", response_model=List[AccountSchema])
def get_accounts(*, session: SessionDep, current_user: CurrentUser):
    """
    **Получает список счетов для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.

    Returns:
        List[AccountSchema]: Список счетов пользователя.
    """
    accounts = session.query(Account).filter(Account.user_id == current_user.id).all()
    return accounts


@router.get(
    "/get_account_transactions/{account_id}", response_model=List[AccountTransactions]
)
def get_account_with_transactions(
    account_id: int,
    current_user: CurrentUser,
    session: SessionDep,
):
    """
    **Получает данные о счёте пользователя вместе с его транзакциями.**

    Args:
        account_id (int): Идентификатор аккаунта.
        current_user (CurrentUser): Авторизованный пользователь.
        session (SessionDep): Сессия базы данных.

    Returns:
        List[AccountTransactions]: Список аккаунтов с их транзакциями.

    Raises:
        HTTPException: Если аккаунт не найден, не принадлежит текущему пользователю
        или если запрос к базе данных завершился ошибкой.
    """
    account = (
        session.query(Account)
        .where(Account.id == account_id, Account.user_id == current_user.id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    statement = (
        select(Account)
        .options(joinedload(Account.transactions))
        .where(Account.id == account_id, Account.user_id == current_user.id)
        .order_by(Account.id)
    )
    transactions = session.execute(statement).unique().scalars().all()
    return transactions


@router.post(
    "/", response_model=AccountSchema
)
def create_account(*, session: SessionDep, account_in: AccountCreate, current_user: CurrentUser):
    """
    **Создает новый счет для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        account_in (AccountCreate): Данные для создания нового счета.

    Returns:
        AccountSchema: Созданный счет.
    """
    account = crud.account.create(db=session, obj_in=account_in, user_id=current_user.id)
    return account


@router.put("/{account_id}", response_model=AccountSchema)
def update_account(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    account_id: int,
    account_in: AccountUpdate,
):
    """
    **Обновляет существующий счет для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        account_id (int): Идентификатор обновляемого счета.
        account_in (AccountUpdate): Данные для обновления счета.

    Returns:
        AccountSchema: Обновленный счет.

    Raises:
        HTTPException: Если счет не найден или пользователь пытается изменить чужой счет.
    """
    account = crud.account.get(session, account_id)
    if not account:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может изменить не свой счёт"
        )

    account = crud.account.update(session, db_obj=account, obj_in=account_in)
    return account


@router.delete("/{account_id}")
def delete_account(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    account_id: int,
):
    """
    **Удаляет счет для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        account_id (int): Идентификатор удаляемого счета.

    Returns:
        str: Сообщение об удалении счета.

    Raises:
        HTTPException: Если счет не найден или пользователь пытается удалить чужой счет.
    """
    account = crud.account.get(session, account_id)
    if not account:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может удалить не свой счёт"
        )

    crud.account.remove(session, id=account_id)
    return f"Счёт: {account.name} удален"
