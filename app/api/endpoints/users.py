from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from app.api.deps import get_current_user, get_session
from app.schemas.user import User

router = APIRouter()


@router.get("/", dependencies=[Depends(get_current_user)], response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
