from fastapi_pagination import Params, paginate, Page
from sqlalchemy.orm import Session

from app.filters.candidate import CandidateFilter
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateReadSchema


def get_candidate_by_email(email: str, db: Session) -> Candidate:
    """
    Retrieve a candidate from the database based on their email.

    Args:
        email (str): The email address of the candidate.
        db (Session): The SQLAlchemy database session for querying.

    Returns:
        Candidate: The Candidate instance associated with the provided email, or None if not found.
    """
    return db.query(Candidate).filter(Candidate.email == email).first()


def get_candidate_by_phone(phone: str, db: Session) -> Candidate:
    """
    Retrieve a candidate from the database based on their phone.

    Args:
        phone (str): The phone number of the candidate.
        db (Session): The SQLAlchemy database session for querying.

    Returns:
        Candidate: The Candidate instance associated with the provided phone, or None if not found.
    """
    return db.query(Candidate).filter(Candidate.phone == phone).first()


def add_new_candidate(candidate: Candidate, db: Session) -> None:
    """
    Add a new candidate to the database.

    Args:
        candidate (Candidate): The candidate instance to be added.
        db (Session): The SQLAlchemy database session.

    Returns:
        None: This function does not return a value.
    """
    db.add(candidate)
    db.commit()


def get_candidate_by_id(id: str, db: Session) -> Candidate:
    """
    Retrieve a candidate from the database by their unique ID.

    Args:
        id (str): The unique ID of the candidate.
        db (Session): The SQLAlchemy database session for querying.

    Returns:
        Candidate: The Candidate instance associated with the given ID, or None if not found.
    """
    return db.get(Candidate, id)


def get_paginated_list_of_candidates(
    db: Session, params: Params
) -> Page[CandidateReadSchema]:
    """
    Retrieve a paginated list of candidates from the database.

    Args:
        db (Session): The SQLAlchemy database session for querying.
        params (Params): Pagination parameters (e.g., page number and size).

    Returns:
        Page[CandidateReadSchema]: A paginated list of candidates.
    """
    return paginate(db.query(Candidate).all(), params=params)


def filter_and_paginate_candidates(
    db: Session, params: Params, candidate_filter: CandidateFilter
) -> Page[CandidateReadSchema]:
    """
    Filter and paginate candidates based on phone, email, and name.

    Args:
        db (Session): The SQLAlchemy database.
        params (Params): Pagination parameters (e.g., page number and size).
        candidate_filter (CandidateFilter): The filter criteria for selecting candidates.

    Returns:
        Page[CandidateReadSchema]: A filtered and paginated list of candidates.
    """

    query = candidate_filter.filter(query=db.query(Candidate))
    return paginate(query.all(), params=params)


def candidate_delete(db: Session, candidate: Candidate) -> None:
    """
    Delete a candidate from the database.

    Args:
        db (Session): The SQLAlchemy database session.
        candidate (Candidate): The candidate instance to be deleted.

    Returns:
        None: This function does not return a value.
    """
    db.delete(candidate)
    db.commit()
