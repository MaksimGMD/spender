from typing import Optional

from faker import Faker
from sqlalchemy.orm import Session

from app.schemas.category import CategoryCreate
from app import crud
from app.models import Category
from app.core.config import settings

fake = Faker()


def create_random_category(db: Session, user_id: Optional[int] = None) -> Category:
    if not user_id:
        user = crud.auth.get_user_by_email(session=db, email=settings.EMAIL_TEST_USER)
        user_id = user.id

    name = fake.word()
    color = fake.color_name()
    icon_name = fake.word()

    category_in = CategoryCreate(name=name, color=color, icon_name=icon_name)
    return crud.category.create(db=db, obj_in=category_in, user_id=user_id)
