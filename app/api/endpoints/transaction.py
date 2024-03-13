from typing import List, Optional
from datetime import datetime
from copy import deepcopy

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.transaction import (
    TransactionSchema,
    TransactionCreate,
    TransactionUpdate,
    TransactionsOut,
    TransactionTransferCreate,
)
from app.schemas.category import CategoryCreate
from app.api.deps import SessionDep, get_current_user, CurrentUser
from app import crud

router = APIRouter()

NOT_FOUND_MESSAGE = "Транзакция не найдена"


@router.get(
    "/{id}",
    dependencies=[Depends(get_current_user)],
    response_model=Optional[TransactionSchema],
)
def get_transaction(*, session: SessionDep, id: int, current_user: CurrentUser):
    """
    **Получает информацию о транзакции по её id.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        id (int): Идентификатор транзакции.
        current_user (CurrentUser): Текущий авторизованный пользователь.

    Returns:
        Optional[TransactionSchema]: Информация о транзакции.

    Raises:
        HTTPException: Если транзакция не найдена или если пользователь пытается получить транзакцию не своего счёта.
    """
    transaction = crud.transaction.get(session, id)

    if not transaction:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    if transaction.account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return transaction


@router.get(
    "/account_transactions/{account_id}",
    dependencies=[Depends(get_current_user)],
    response_model=List[TransactionsOut],
)
def get_account_transactions(
    *,
    session: SessionDep,
    account_id: int,
    begin_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    transaction_type: Optional[str] = Query(
        None,
        description="Фильтрует транзакции по типу: 'income' - доходы или 'expense' - расходы",
    ),
):
    """
    **Получает список транзакций для указанного счёта с возможностью фильтрации.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        account_id (int): Идентификатор счёта.
        begin_date (Optional[datetime], optional): Начальная дата фильтрации. Defaults to None.
        end_date (Optional[datetime], optional): Конечная дата фильтрации. Defaults to None.
        transaction_type (Optional[str], optional): Тип транзакции для фильтрации: 'income' - доходы, 'expense' - расходы. Defaults to None.

    Returns:
        List[TransactionsOut]: Список транзакций.

    Raises:
        HTTPException: Если произошла ошибка при получении транзакций.
    """
    return crud.transaction.get_filtered_transactions(
        session, account_id, begin_date, end_date, transaction_type
    )


@router.post(
    "/", dependencies=[Depends(get_current_user)], response_model=TransactionSchema
)
def create_transaction(*, session: SessionDep, transaction_in: TransactionCreate):
    """
    **Создает новую транзакцию для текущего пользователя.
    Если amount положительная - доход. Если amount отрицательная - расход**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        transaction_in (TransactionCreate): Данные для создания новой транзакции.

    Returns:
        TransactionSchema: Созданная транзакция.

    Raises:
        HTTPException: В случае ошибки при создании транзакции.
    """
    try:
        transaction = crud.transaction.create(db=session, obj_in=transaction_in)
        return transaction
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}") from e


@router.put("/{transaction_id}", response_model=TransactionSchema)
def update_transaction(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    transaction_id: int,
    transaction_in: TransactionUpdate,
):
    """
    **Обновляет существующую транзакцию пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        transaction_id (int): Идентификатор транзакции.
        transaction_in (TransactionUpdate): Данные для обновления транзакции.

    Returns:
        TransactionSchema: Обновлённая транзакция.

    Raises:
        HTTPException: Если транзакция не найдена, пользователь не может изменить транзакцию не своего счёта,
        или произошла ошибка при обновлении транзакции.
    """
    transaction = crud.transaction.get(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    if transaction.account.user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не может изменить транзакцию не своего счёта",
        )

    try:
        transaction = crud.transaction.update(
            session, db_obj=transaction, obj_in=transaction_in
        )
        crud.account.update_balance(session, transaction.account_id)
        return transaction
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}") from e


@router.delete("/{transaction_id}")
def delete_transaction(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    transaction_id: int,
):
    """
    **Удаляет транзакцию пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        transaction_id (int): Идентификатор транзакции.

    Returns:
        str: Сообщение об успешном удалении транзакции.

    Raises:
        HTTPException: Если транзакция не найдена, пользователь не может удалить транзакцию не своего счёта,
        или произошла ошибка при удалении транзакции.
    """
    transaction = crud.transaction.get(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    if transaction.account.user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не может удалить транзакцию не своего счёта",
        )
    try:
        crud.transaction.remove(session, id=transaction_id)
        crud.account.update_balance(session, transaction.account_id)
        return f"Транзакция на сумму: {transaction.amount}, выполненная: {transaction.date} удалена"
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}") from e


@router.post(
    "/transfer_transaction",
    response_model=str,
)
def create_transfer_transaction(
    *,
    session: SessionDep,
    transaction_in: TransactionTransferCreate,
    current_user: CurrentUser,
):
    """
    **Создает новую транзакцию для перевода денег между счетами текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        transaction_in (TransactionCreate): Данные для создания новой транзакции.
        current_user (CurrentUser): Текущий авторизованный пользователь.

    Returns:
        TransactionSchema: Созданная транзакция.

    Raises:
        HTTPException: В случае ошибки при создании транзакции.
    """
    # Получает данные о счетах
    account_from = crud.account.get(session, transaction_in.account_id)
    if not account_from:
        raise HTTPException(status_code=404, detail="Счёт отправитель не найден")

    account_to = crud.account.get(session, transaction_in.to_account_id)
    if not account_to:
        raise HTTPException(status_code=404, detail="Счёт получатель не найден")

    if account_from.user_id != current_user.id or account_to.user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не может сделать перевод не для своих счетов",
        )
    # Проверяет наличие категории для перевода
    translation_category = crud.category.get_by_name(session, "Перевод")
    if not translation_category:
        translation_category = crud.category.create(
            db=session,
            obj_in=CategoryCreate(name="Перевод", user_id=current_user.id),
        )

    # Добавялет идентификатор категории
    transaction_in.category_id = translation_category.id
    transaction_in_dump = transaction_in.model_dump()
    # Убирает не валидное поле
    transaction_in_dump.pop("to_account_id")

    # Создаёт транзакцию для счёта отправителя
    crud.transaction.create(db=session, obj_in=transaction_in_dump)

    to_transaction_in = transaction_in.model_copy(deep=True)
    to_transaction_in.amount = -transaction_in.amount
    to_transaction_in.account_id = transaction_in.to_account_id
    to_transaction_in_dump = transaction_in.model_dump()
    to_transaction_in_dump.pop("to_account_id")
    try:

        # Создаёт транзакцию для счёта получателя
        crud.transaction.create(db=session, obj_in=to_transaction_in_dump)

        return f"Перевод на сумму {transaction_in.amount}, {account_from.name} --> {account_to.name}, прошёл успешно"
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}") from e
