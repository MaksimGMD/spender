from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.crud.base import CRUDBase
from app.crud import account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.schemas.account import AccountUpdateBalance
from app.models.user import User
from app.models.account import Account
from app.models.category import Category


class CRUDtransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def create(self, db: Session, *, obj_in: TransactionCreate):
        new_transaction = super().create(db, obj_in=obj_in)
        new_amount = AccountUpdateBalance(
            id=new_transaction.account_id,
            amount=new_transaction.amount,
        )
        account.update_balance_by_transaction(db=db, obj_in=new_amount)
        return super().create(db, obj_in=obj_in)

    def get_filtered_transactions(
        self,
        db: Session,
        account_id: int,
        begin_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        transaction_type: Optional[str] = None,
    ):
        statement = (
            select(
                Transaction.id,
                Transaction.amount,
                Transaction.date,
                Transaction.description,
                Transaction.category_id,
                Transaction.account_id,
                Category.name.label("category_name"),
                Account.name.label("account_name"),
            )
            .join(Account)
            .join(Category)
            .where(Transaction.account_id == account_id)
        )

        if begin_date:
            statement = statement.where(Transaction.date >= begin_date)
        if end_date:
            statement = statement.where(Transaction.date <= end_date)
        if transaction_type:
            if transaction_type.lower() == "income":
                statement = statement.where(Transaction.amount >= 0)
            elif transaction_type.lower() == "expense":
                statement = statement.where(Transaction.amount < 0)

        statement = statement.order_by(Transaction.date.desc())

        transactions = db.execute(statement).all()
        return transactions


transaction = CRUDtransaction(Transaction)
