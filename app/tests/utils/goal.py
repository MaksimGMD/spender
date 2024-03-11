from typing import Optional
from faker import Faker
from sqlalchemy.orm import Session

from app.schemas.goal import GoalCreate
from app import crud
from app.core.config import settings
from app.models import Goal

fake = Faker()


def create_random_goal(db: Session, user_id: Optional[int] = None) -> Goal:
    if not user_id:
        user = crud.auth.get_user_by_email(session=db, email=settings.EMAIL_TEST_USER)
        user_id = user.id

    name = fake.word()
    target_amount = fake.pydecimal(min_value=1, max_value=10000, right_digits=2)
    amount = fake.pydecimal(min_value=0, max_value=target_amount, right_digits=2)

    goal_in = GoalCreate(
        name=name,
        target_amount=target_amount,
        amount=amount,
        user_id=user_id,
    )

    return crud.goal.create(db=db, obj_in=goal_in, user_id=user_id)
