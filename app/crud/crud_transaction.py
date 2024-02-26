from sqlalchemy.orm import Session
from sqlmodel import select

from app.crud.base import CRUDBase
from app.crud import account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.schemas.account import AccountUpdateBalance
from app.models.user import User
from app.models.account import Account


class CRUDtransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def create(self, db: Session, *, obj_in: TransactionCreate):
        new_transaction = super().create(db, obj_in=obj_in)
        new_amount = AccountUpdateBalance(
            id=new_transaction.account_id,
            amount=new_transaction.amount,
        )
        account.update_balance_by_transaction(db=db, obj_in=new_amount)
        return super().create(db, obj_in=obj_in)

    def get_user_id_by_account(self, db: Session, account_id: int):
        statement = (
            select(User.id)
            .join(Account, User.id == Account.user_id)
            .where(Account.id == account_id)
        )

        return db.exec(statement).first()


transaction = CRUDtransaction(Transaction)
