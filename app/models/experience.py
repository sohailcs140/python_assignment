from sqlalchemy import String, Column, ForeignKey, Date, Integer
from sqlalchemy.orm import Relationship

from app.db.database import Base
from app.models.candidate import Candidate


class Experience(Base):
    __tablename__ = 'experience'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True, default=None)
    candidate_id = Column(String, ForeignKey('candidates.id', ondelete='CASCADE'))

    candidate = Relationship(Candidate, back_populates='experience')
