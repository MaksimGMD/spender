from typing import Optional
from faker import Faker
from sqlalchemy.orm import Session

from app.schemas.transaction import TransactionCreate
from app import crud
from app.core.config import settings
from app.models import Transaction
from app.tests.utils.category import create_random_category
from app.tests.utils.account import create_random_account

fake = Faker()


def create_random_transaction(
    db: Session, user_id: Optional[int] = None
) -> Transaction:
    if not user_id:
        user = crud.auth.get_user_by_email(session=db, email=settings.EMAIL_TEST_USER)
        user_id = user.id

    amount = fake.pydecimal(min_value=-1000, max_value=1000, right_digits=2)
    description = fake.word()

    category = create_random_category(db=db, user_id=user_id)
    account = create_random_account(db=db, user_id=user_id)

    transaction_in = TransactionCreate(
        amount=amount,
        description=description,
        category_id=category.id,
        account_id=account.id,
    )

    return crud.transaction.create(db=db, obj_in=transaction_in, user_id=user_id)
