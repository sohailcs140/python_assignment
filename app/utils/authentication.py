import os
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db_queries.user_queries import get_user_by_email
from app.models.user import User
from app.schemas.user import TokenData, Token
from app.utils import constants

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def create_access_token(user_data: dict, expires_minutes: int = 30) -> str:
    """
    Create a JSON Web Token (JWT) access token for the given user data.

    Args:
        user_data (dict): A dictionary containing user information to be encoded in the token.
        expires_minutes (int, optional): The expiration time for the token in minutes. Defaults to 30 minutes.

    Returns:
        str: The encoded JWT access token.

    Raises:
        Exception: May raise an exception if encoding the token fails.
    """
    user_data.update(
        {"exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)}
    )
    return jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)


def varify_token(token: str, db: Session) -> User:
    """
    Verify the validity of a JSON Web Token (JWT).

    Args:
        db: database session.
        token (str): The JWT to be verified.

    Returns:
        User: user if the token is valid; otherwise, an exception is raised.

    Raises:
        HTTPException: Raises an HTTP 401 Unauthorized error if the token is expired,
                       invalid, or does not contain an email.
    """
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.TOKEN_EXPIRE_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.UNAUTHORIZED_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.UNAUTHORIZED_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(value=email, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.UNAUTHORIZED_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_password_hash(password: str) -> str:
    """
    Generate a hashed password from the given plain text password.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed version of the provided password.
    """
    return pwd_context.hash(password)


def varify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password; otherwise, False.
    """
    return pwd_context.verify(password, hashed_password)


def authenticate_user(
    email: str, password: str, db: Session = Depends(get_db)
) -> User | bool:
    """
    Authenticate a user by verifying their email and password.

    Args:
        email (str): The email address of the user attempting to authenticate.
        password (str): The plain text password provided by the user.
        db: database session.

    Returns:
        User | bool: The authenticated User object if successful; otherwise, False.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not varify_password(password, user.password):
        return False

    return user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token used for authentication, provided by the OAuth2 scheme.
        db (Session): database session.

    Raises:
        HTTPException: Raises an HTTP 401 Unauthorized error if the token is invalid or the user cannot be found.

    Returns:
        User: The authenticated User object associated with the provided token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(value=token_data.email, db=db)
    if not user:
        raise credentials_exception
    return user


def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    """
    Log in a user and issue an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the user's email and password.
        db (Session): The database session.

    Raises:
        HTTPException: Raises an HTTP 401 Unauthorized error if the credentials are incorrect.

    Returns:
        Token: An object containing the access token and its type.
    """
    user = authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_data={"email": user.email})
    return Token(access_token=access_token, token_type="bearer")
