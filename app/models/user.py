from app.db.database import BaseModel
from sqlalchemy import Column, String


class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
