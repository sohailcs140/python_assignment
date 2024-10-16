from typing import Dict

from fastapi import HTTPException, status
from fastapi_pagination import Params, Page
from sqlalchemy.orm import Session

from app.celery.tasks import generate_candidates_csv_file
from app.db_queries.candidate_queries import (
    add_new_candidate,
    get_candidate_by_email,
    get_candidate_by_id,
    get_candidate_by_phone,
    get_paginated_list_of_candidates,
    candidate_delete,
    filter_and_paginate_candidates,
)
from app.filters.candidate import CandidateFilter
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateSchema, CandidateReadSchema
from app.utils import constants


def create_candidate(body: CandidateSchema, db: Session) -> Candidate:
    """
    Creates a new candidate in the database.

    Args:
        body (CandidateSchema): The candidate data, including name, email, and phone number.
        db (Session): The SQLAlchemy database session.

    Returns:
        Candidate: The newly created candidate object.

    Raises:
        HTTPException: If the email or phone number is already in use,
                       or if there is a failure during candidate creation.
    """
    if get_candidate_by_email(email=body.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.EMAIL_ALREADY_INUSE_MESSAGE,
        )

    if get_candidate_by_phone(phone=body.phone, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.PHONE_NUMBER_ALREAY_INUSE_MESSAGE,
        )

    candidate = Candidate(name=body.name, email=body.email, phone=body.phone)

    add_new_candidate(candidate=candidate, db=db)

    return candidate


def retrieve_candidate(candidate_id: str, db: Session) -> Candidate:
    """
    Retrieve a candidate from the database by their unique identifier.

    Args:
        candidate_id (str): The unique identifier of the candidate to retrieve.
        db (Session): The SQLAlchemy database session used for database operations.

    Returns:
        Candidate: The candidate object retrieved from the database, including
                   associated skills and experience.

    Raises:
        HTTPException: If no candidate is found with the provided ID, a
                       404 Not Found error is raised.
    """

    candidate = get_candidate_by_id(id=candidate_id, db=db)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found."
        )

    return candidate


def list_candidates(db: Session, params: Params) -> Page[CandidateReadSchema]:
    """
    Retrieve a paginated list of candidates from the database.

    Args:
        db (Session): The SQLAlchemy database session used for database operations.
        params (Params): The parameters for pagination, including page number and page size.

    Returns:
        Page[CandidateReadSchema]: A paginated list of candidates, including their details.

    Raises:
        HTTPException: If there is an issue with retrieving the candidates.
    """
    return get_paginated_list_of_candidates(db=db, params=params)


def filter_candidates(
    db: Session, params: Params, candidate_filter: CandidateFilter
) -> Page[CandidateReadSchema]:
    """
    Retrieve a paginated list of candidates based on specified filters.

    Args:
        db (Session): The SQLAlchemy database session used for database operations.
        params (Params): The parameters for pagination, including page number and page size.
        candidate_filter (CandidateFilter): The filter criteria to apply to the candidate query.

    Returns:
        Page[CandidateReadSchema]: A paginated list of candidates that match the specified filters.

    Raises:
        HTTPException: If there is an issue with filtering the candidates.
    """

    return filter_and_paginate_candidates(
        db=db, params=params, candidate_filter=candidate_filter
    )


def delete_candidate(candidate_id: str, db: Session) -> Dict:
    """
    Delete a candidate from the database by their unique identifier.

    Args:
        candidate_id (str): The unique identifier of the candidate to delete.
        db (Session): The SQLAlchemy database session used for database operations.

    Returns:
        None: This function does not return a value.

    Raises:
        HTTPException: If no candidate is found with the provided ID, a
                       404 Not Found error is raised.
    """

    candidate = get_candidate_by_id(db=db, id=candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found."
        )

    candidate_delete(candidate=candidate, db=db)

    return {"message": "candidate deleted."}


def generate_candidates_report(db: Session) -> dict[str, str]:
    """
    Initiate the generation of a candidates report in CSV format.

    Args:
        db (Session): The SQLAlchemy database session.

    Returns:
        str: A message indicating that the report generation has been initiated.

    Raises:
        HTTPException: If there is an issue with starting the report generation.
    """

    generate_candidates_csv_file.delay()

    return {"message": "Generating report..."}
