from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserSchema
from app.utils import constants
from app.utils.authentication import create_access_token, get_password_hash, varify_password


def create(body: UserSchema, db: Session, password_hash=get_password_hash(body.password)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already taken.")

    hash_password = password_hash
    access_token = create_access_token({'email': body.email})

    user = User(email=body.email, password=hash_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {'email': user.email, 'access_token': access_token}


def login(body: UserSchema, db: Session):
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=constants.UNAUTHORIZED_MESSAGE)

    if not varify_password(password=body.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=constants.UNAUTHORIZED_MESSAGE)

    access_token = create_access_token({'email': user.email})

    return {'access_token': access_token}
