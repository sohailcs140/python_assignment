from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserSchema
from app.services import user

router = APIRouter(prefix='/users')


@router.post("/register")
def register(body: UserSchema, db: Session = Depends(get_db)):
    return user_services.create(body=body, db=db)

@router.post('/login')
def login(body:UserSchema, db:Session = Depends(get_db)):
    return user_services.login(body=body, db=db)