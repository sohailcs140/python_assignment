from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.candidate import (
    SkillUpdateSchema,
    SkillSchema,
    SkillReadSchema,
    SkillReadSchemaWithCandidateId,
)
from app.services import skill as skill_service
from app.utils import authentication

skill_router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
    dependencies=[Depends(authentication.get_current_user)],
)


@skill_router.post(
    "/", response_model=SkillReadSchema, status_code=status.HTTP_201_CREATED
)
def create_skill(request_body: SkillSchema, db: Session = Depends(get_db)):
    return skill_service.create_skill(request_body=request_body, db=db)


@skill_router.get(
    "/{skill_id}", response_model=SkillReadSchema, status_code=status.HTTP_200_OK
)
def retrieve_skill(skill_id: int, db: Session = Depends(get_db)):
    return skill_service.retrieve_skill(skill_id=skill_id, db=db)


@skill_router.get(
    "/candidate/{candidate_id}",
    response_model=Page[SkillReadSchemaWithCandidateId],
    status_code=status.HTTP_200_OK,
)
def list_skills(
    candidate_id: str, db: Session = Depends(get_db), params: Params = Depends()
):
    return skill_service.list_skills(candidate_id=candidate_id, db=db, params=params)


@skill_router.put("/{skill_id}/update", status_code=status.HTTP_200_OK)
def update_skill(
    request_body: SkillUpdateSchema, skill_id: int, db: Session = Depends(get_db)
):
    return skill_service.update_skill(
        request_body=request_body, skill_id=skill_id, db=db
    )


@skill_router.delete("/{skill_id}/delete/", status_code=status.HTTP_200_OK)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    return skill_service.delete_skill(skill_id=skill_id, db=db)
