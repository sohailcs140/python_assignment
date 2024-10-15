from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserSchema
from app.services import user as user_services
from app.utils import authentication

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return user_services.register(body=body, db=db)


@router.post("/login")
def login(body: UserSchema, db: Session = Depends(get_db)):
    return user_services.login(body=body, db=db)


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    return authentication.login_for_access_token(form_data=form_data, db=db)
