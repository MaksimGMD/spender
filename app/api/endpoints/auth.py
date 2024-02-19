from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_session
from app.core.security import create_access_token
from app.crud.auth import authenticate
from app.models.token import Token


router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя или пароль")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }
