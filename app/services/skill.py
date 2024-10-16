from fastapi import Depends, HTTPException, status
from fastapi_pagination import Params, Page
from sqlalchemy.orm import Session

from app.db_queries.candidate_queries import get_candidate_by_id
from app.db_queries.skill_queries import (
    add_new_skill,
    get_skill_by_id,
    get_paginated_list_of_skills,
    skill_delete,
    skill_update,
)
from app.models.skills import Skill
from app.schemas.candidate import (
    SkillSchema,
    SkillReadSchemaWithCandidateId,
    SkillUpdateSchema,
)


def create_skill(request_body: SkillSchema, db: Session) -> Skill:
    """
    Create a new skill in the database.

    Args:
        request_body (SkillSchema): The skill data.
        db (Session): The SQLAlchemy database session.

    Returns:
        Skill: The newly created skill object.

    Raises:
        HTTPException: If there is an issue with creating the skill in the database.
    """
    candidate = get_candidate_by_id(
        id=request_body.model_dump().get("candidate_id"), db=db
    )

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found."
        )

    new_skill = Skill(**request_body.model_dump())

    return add_new_skill(db=db, skill=new_skill)


def retrieve_skill(skill_id: int, db: Session) -> Skill:
    """
    Retrieve a skill from the database by its unique ID.

    Args:
        skill_id (str): The unique identifier of the skill.
        db (Session): The SQLAlchemy database session.

    Returns:
        Skill: The retrieved skill object.

    Raises:
        HTTPException: If no skill is found, a 404 Not Found error is raised.
    """

    skill = get_skill_by_id(id=skill_id, db=db)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found."
        )

    return skill


def list_skills(
    candidate_id: str, db: Session, params: Params = Depends()
) -> Page[SkillReadSchemaWithCandidateId]:
    """
    Retrieve a paginated list of skills for a specific candidate.

    Args:
        candidate_id (str): The unique identifier of the candidate.
        db (Session): The SQLAlchemy database session.
        params (Params): Pagination parameters, including page number and size.

    Returns:
        Page[Skill]: A paginated list of skills for the specified candidate.

    Raises:
        HTTPException: If no candidate is found, a 404 Not Found error is raised.
    """

    candidate = get_candidate_by_id(id=candidate_id, db=db)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found."
        )

    return get_paginated_list_of_skills(candidate=candidate, params=params)


def delete_skill(skill_id: int, db: Session) -> dict[str, str]:
    """
    Delete a skill from the database by its unique ID.

    Args:
        skill_id (str): The unique identifier of the skill.
        db (Session): The SQLAlchemy database session.

    Returns:
        None: Indicates that the skill has been deleted.

    Raises:
        HTTPException: If no skill is found, a 404 Not Found error is raised.
    """

    if not get_skill_by_id(id=skill_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found."
        )

    skill_delete(id=skill_id, db=db)

    return {"message": "skill deleted."}


def update_skill(request_body: SkillUpdateSchema, skill_id: int, db: Session) -> Skill:
    """
    Update an existing skill in the database.

    Args:
        request_body (SkillUpdateSchema): The updated skill data with attributes to modify.
        skill_id (str): The unique identifier of the skill to update.
        db (Session): The SQLAlchemy database session.

    Returns:
        Skill: The updated skill object.

    Raises:
        HTTPException: If no skill is found, a 404 Not Found error is raised.
    """
    if not get_skill_by_id(id=skill_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found."
        )

    skill = skill_update(id=skill_id, request_body=request_body, db=db)

    return skill
