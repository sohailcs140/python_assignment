from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import Token
from app.schemas.user import UserSchema
from app.utils import constants
from app.utils.authentication import create_access_token, get_password_hash, authenticate_user


def register(body: UserSchema, db: Session) -> Token:
    """
    Register a new user.

    This function checks if the provided email is already in use. If not,
    it hashes the user's password, creates a new user record, and
    generates an access token.

    :param body: The user data, including email and password.
    :param db: The SQLAlchemy database session used for database operations.
    :return: A Token object containing the type of token and the access token.

    :raises HTTPException: If the email is already taken, a 400 Bad Request error
                          is raised.
    """

    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already taken.")

    hash_password = get_password_hash(body.password)
    access_token = create_access_token({'email': body.email})

    user = User(email=body.email, password=hash_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return Token(token_type='bearer', access_token=access_token)


def login(body: UserSchema, db: Session = Depends(get_db)) -> Token:
    """
    Authenticate a user and generate an access token.

    This function checks if the user exists and verifies the provided
    password. If authentication is successful, it generates and returns
    an access token.

    :param body: The user data, including email and password.
    :param db: The SQLAlchemy database session used for database operations.
                Defaults to the database session provided by FastAPI's dependency injection.
    :return: A Token object containing the type of token and the access token.

    :raises HTTPException: If the user does not exist or if the authentication
                          fails, a 401 Unauthorized error is raised.
    """
    user = db.query(User).filter(User.email == body.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=constants.UNAUTHORIZED_MESSAGE)

    if not authenticate_user(email=user.email, password=body.password, db=db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=constants.UNAUTHORIZED_MESSAGE)

    access_token = create_access_token({'email': user.email})

    return Token(token_type='bearer', access_token=access_token)
