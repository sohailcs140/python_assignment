import os
from datetime import timedelta, datetime, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.utils import constants

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def varify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
