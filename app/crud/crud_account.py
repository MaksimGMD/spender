from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate, AccountUpdateBalance
from app.models.transaction import Transaction


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def update_balance_by_transaction(
        self, db: Session, *, obj_in: AccountUpdateBalance
    ) -> Account:
        """
        Обновляет баланс счета на основе изменения транзакции.

        Args:
            db (Session): Сессия базы данных.
            obj_in (AccountUpdateBalance): Данные для обновления баланса.

        Returns:
            Account: Обновленный объект счета.
        """
        account = super().get(db, id=obj_in.id)

        if account:
            account.balance += obj_in.amount
            db.commit()
            db.refresh(account)

        return account

    def update_balance(self, db: Session, account_id: int):
        """
        Обновляет баланс счета на основе суммы транзакций.

        Args:
            db (Session): Сессия базы данных.
            account_id (int): Идентификатор счета.

        Returns:
            Account: Обновленный объект счета.
        """
        account = super().get(db, id=account_id)
        if account:
            transactions = (
                db.query(Transaction).filter(Transaction.account_id == account_id).all()
            )

            new_balance = account.balance
            for transaction in transactions:
                new_balance += transaction.amount
            account.balance = new_balance
            db.commit()
            db.refresh(account)
            return account


account = CRUDAccount(Account)
