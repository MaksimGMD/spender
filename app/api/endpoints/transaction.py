from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionSchema,
    TransactionCreate,
    TransactionUpdate,
)
from app.api.deps import get_current_user, get_session, CurrentUser
from app import crud

router = APIRouter()


@router.get("/", response_model=List[TransactionSchema])
def get_transactions(
    *, session: Session = Depends(get_session), current_user: CurrentUser
):

    transactions = session.exec(select(Transaction)).all()
    return transactions


@router.post(
    "/", dependencies=[Depends(get_current_user)], response_model=TransactionSchema
)
def create_transaction(
    *, session: Session = Depends(get_session), transaction_in: TransactionCreate
):
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
    session: Session = Depends(get_session),
    current_user: CurrentUser,
    transaction_id: int,
    transaction_in: TransactionUpdate,
):
    transaction = crud.transaction.get(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    user_id = crud.transaction.get_user_id_by_account(
        db=session, account_id=transaction.account_id
    )
    if user_id != current_user.id:
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
    session: Session = Depends(get_session),
    current_user: CurrentUser,
    transaction_id: int,
):
    transaction = crud.transaction.get(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    user_id = crud.transaction.get_user_id_by_account(
        db=session, account_id=transaction.account_id
    )
    if user_id != current_user.id:
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
