from typing import Optional
from faker import Faker
from sqlalchemy.orm import Session

from app.schemas.account import AccountCreate, CurrencyEnum
from app import crud
from app.core.config import settings
from app.models import Account

fake = Faker()


def create_random_account(db: Session, user_id: Optional[int] = None) -> Account:
    if not user_id:
        user = crud.auth.get_user_by_email(session=db, email=settings.EMAIL_TEST_USER)
        user_id = user.id

    name = fake.word()
    balance = fake.pydecimal(min_value=0, max_value=10000, right_digits=2)
    currency = fake.random_element(elements=[c.value for c in CurrencyEnum])
    account_type = fake.word()
    is_active = fake.boolean()

    account_in = AccountCreate(
        name=name,
        balance=balance,
        currency=currency,
        type=account_type,
        is_active=is_active,
        user_id=user_id,
    )

    return crud.account.create(db=db, obj_in=account_in, user_id=user_id)
