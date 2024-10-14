import os
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import TokenData, Token
from app.utils import constants

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


def create_access_token(user_data: dict, expires_minutes: int = 30) -> str:
    user_data.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)})
    return jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)


def varify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('email')


    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=constants.TOKEN_EXPIRE_MESSAGE,
                            headers={"WWW-Authenticate": "Bearer"})
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=constants.UNAUTHORIZED_MESSAGE,
                            headers={"WWW-Authenticate": "Bearer"})
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=constants.UNAUTHORIZED_MESSAGE,
                            headers={"WWW-Authenticate": "Bearer"})

    return True


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def varify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not varify_password(password, user.password):
        return False

    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_data={"email": user.email})
    return Token(access_token=access_token, token_type="bearer")
