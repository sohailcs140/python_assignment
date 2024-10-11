from datetime import datetime, date
from typing import List

from pydantic import BaseModel, EmailStr


class SkillSchema(BaseModel):
    name: str


class ExperienceSchema(BaseModel):
    job_title: str
    company: str
    start_date: date
    end_date: date


class CandidateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str



class CandidateReadSchema(CandidateSchema):
    create_at: datetime
    update_at: datetime
    skills: List[SkillSchema]
    experience:List[ExperienceSchema]

    class Config:
        from_attributes=True


