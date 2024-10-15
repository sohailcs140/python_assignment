from fastapi_pagination import Params, paginate
from sqlalchemy.orm import Session

from app.models import Candidate
from app.models.skills import Skill
from app.schemas.candidate import SkillUpdateSchema


def add_new_skill(db: Session, skill: Skill) -> Skill:
    """
    Add a new skill to the database.

    Args:
        db (Session): The SQLAlchemy database session.
        skill (Skill): The Skill instance to be saved in the database.

    Returns:
        Skill: The added Skill instance.
    """
    db.add(skill)
    db.commit()

    return skill


def get_skill_by_id(id: int, db: Session) -> Skill:
    """
    Retrieve a Skill instance from the database by its unique ID.

    Args:
        id (int): The unique ID of the skill.
        db (Session): The database session.

    Returns:
        Skill: The Skill instance associated with the given ID, or None if not found.
    """
    return db.get(Skill, id)


def get_paginated_list_of_skills(candidate: Candidate, params: Params):
    """
    Retrieve a paginated list of skills for a given candidate.

    Args:
        candidate (Candidate): The candidate instance whose skills are to be retrieved.
        params (Params): Pagination parameters (e.g., page number and size).

    Returns:
        Page[Skills]: A paginated list of Skills associated with the candidate.
    """
    return paginate(candidate.skills, params=params)


def skill_delete(id: int, db: Session) -> None:
    """
    Delete a skill from the database by its unique ID.

    Args:
        id (int): The unique ID of the skill to be deleted.
        db (Session): The database session.

    Returns:
        None: This function does not return a value.

    """
    skill = get_skill_by_id(id=id, db=db)

    db.delete(skill)
    db.commit()


def skill_update(id: int, request_body: SkillUpdateSchema, db: Session) -> Skill:
    """
    Update a skill in the database.

    Args:
        id (int): The unique ID of the skill to update.
        request_body (SkillUpdateSchema): The new data for the skill.
        db (Session): The database session.

    Returns:
        Skill: The updated Skill instance.

    Raises:
        ValueError: If no skill with the given ID exists.
    """
    skill = get_skill_by_id(id=id, db=db)

    for key, value in request_body.model_dump().items():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)

    return skill
