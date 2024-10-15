from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db_queries.user_queries import get_user_by_email, register_new_user
from app.models.user import User
from app.schemas.user import Token
from app.schemas.user import UserSchema
from app.utils import constants
from app.utils.authentication import (
    create_access_token,
    get_password_hash,
    authenticate_user,
)


def register(body: UserSchema, db: Session) -> Token:
    """
    Register a new user.

    Args:
        body (UserSchema): The user data, including email and password.
        db (Session): The SQLAlchemy database session.

    Returns:
        Token: A Token object containing the token type and access token.

    Raises:
        HTTPException: If the email is already taken, a 400 Bad Request error is raised.
    """

    if get_user_by_email(value=body.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="email already taken."
        )

    hash_password = get_password_hash(body.password)
    access_token = create_access_token({"email": body.email})

    user = User(email=body.email, password=hash_password)

    register_new_user(user=user, db=db)

    return Token(token_type="bearer", access_token=access_token)


def login(body: UserSchema, db: Session) -> Token:
    """
    Authenticate a user and generate an access token.

    Args:
        body (OAuth2PasswordRequestForm): The user data, including email and password.
        db (Session): The SQLAlchemy database session.

    Returns:
        Token: A Token object containing the token type and access token.

    Raises:
        HTTPException: If the user does not exist or authentication fails, a 401 Unauthorized error is raised.
    """

    user = get_user_by_email(value=body.email, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.UNAUTHORIZED_MESSAGE,
        )

    if not authenticate_user(email=user.email, password=body.password, db=db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.UNAUTHORIZED_MESSAGE,
        )

    access_token = create_access_token({"email": user.email})

    return Token(token_type="bearer", access_token=access_token)
