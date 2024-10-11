from sqlalchemy import String, Column
from sqlalchemy.orm import Relationship

from app.db.database import BaseModel


class Candidate(BaseModel):
    __tablename__ = "candidates"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String(15), nullable=False, unique=True)

    skills = Relationship('Skill', back_populates='candidate', uselist=True)
    experience = Relationship('Experience', back_populates='candidate', uselist=True)
