from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import Relationship

from app.db.database import Base
from app.models.candidate import Candidate


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    candidate_id = Column(String, ForeignKey("candidates.id", ondelete="CASCADE"))
    candidate = Relationship(Candidate, back_populates="skills")
