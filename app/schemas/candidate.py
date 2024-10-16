from datetime import datetime, date
from typing import List

from pydantic import BaseModel, EmailStr


class CandidateSkillSchema(BaseModel):
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
    id: str
    create_at: datetime
    update_at: datetime
    skills: List[CandidateSkillSchema]
    experience: List[ExperienceSchema]

    class Config:
        from_attributes = True


# Skill Schemas


class SkillSchema(BaseModel):
    name: str
    candidate_id: str


class SkillUpdateSchema(BaseModel):
    name: str


class SkillReadSchema(BaseModel):
    name: str
    id: int

    class Config:
        from_attributes = True


class SkillReadSchemaWithCandidateId(BaseModel):
    candidate_id: str
    name: str
    id: int

    class Config:
        from_attributes = True
