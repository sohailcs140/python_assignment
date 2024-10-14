from http.client import HTTPException

from fastapi import Depends, HTTPException, status
from fastapi_pagination import Params, paginate, Page
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Candidate
from app.models.skills import Skill
from app.schemas.candidate import (SkillSchema, SkillReadSchemaWithCandidateId)


def create_skill(request_body: SkillSchema, db: Session = Depends(get_db)) -> Skill:
    """
    Create a new skill in the database.

    :param request_body: The skill data, including attributes like name and candidate_id.
    :param db: The SQLAlchemy database session used for database operations.

    :return: The newly created skill object.

    :raises HTTPException: If there is an issue with creating the skill in the database.
    """
    new_skill = Skill(**request_body.model_dump())
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


def retrieve_skill(skill_id: int, db: Session = Depends(get_db)) -> Skill:
    """
    Retrieve a skill from the database by its unique identifier (id).

    :param skill_id: The unique identifier of the skill to retrieve.
    :param db: The SQLAlchemy database session used for database operations.

    :return: The skill object retrieved from the database.

    :raises HTTPException: If no skill is found with the provided ID, a
                          404 Not Found error is raised.
    """
    skill = db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found.')

    return skill


def list_skills(candidate_id: str, db: Session = Depends(get_db),
                params: Params = Depends()) -> Page[SkillReadSchemaWithCandidateId]:
    """
    Retrieve a paginated list of skills for a specific candidate.

    :param candidate_id: The unique identifier of the candidate whose skills
                         are to be retrieved.
    :param db: The SQLAlchemy database session used for database operations.

    :param params: The parameters for pagination, including page number and
                   page size.
    :return: A paginated list of skills associated with the specified candidate.

    :raises HTTPException: If no candidate is found with the provided ID, a
                          404 Not Found error is raised.
    """
    candidate = db.get(Candidate, candidate_id)

    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Candidate not found.')

    return paginate(candidate.skills, params=params)


def delete_skill(skill_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete a skill from the database by its unique identifier (id).
    
    :param skill_id: The unique identifier of the skill to delete.
    :param db: The SQLAlchemy database session used for database operations.
    
    :return: A message indicating that the skill has been deleted.

    :raises HTTPException: If no skill is found with the provided ID, a 
                         404 Not Found error is raised.
    """
    skill = retrieve_skill(skill_id=skill_id, db=db)

    db.delete(skill)
    db.commit()

    return {'message': 'skill deleted.'}


def update_skill(request_body: SkillSchema, skill_id: int, db: Session = Depends(get_db)) -> Skill:
    """
    Update an existing skill in the database.

    :param request_body: The updated skill data, including attributes to modify.
    :param skill_id: The unique identifier of the skill to update.
    :param db: The SQLAlchemy database session used for database operations.

    :return: The updated skill object.

    :raises HTTPException: If no skill is found with the provided ID, a
                          404 Not Found error is raised.
    """
    skill = retrieve_skill(skill_id=skill_id, db=db)

    for key, value in request_body.model_dump().items():
        setattr(skill, key, value)

    db.commit()

    db.refresh(skill)

    return skill
