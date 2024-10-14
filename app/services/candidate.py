from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi_pagination import Params, paginate, Page
from sqlalchemy.orm import Session, joinedload

from app.celery.tasks import generate_candidates_csv_file
from app.db.database import get_db
from app.filters.candidate import CandidateFilter
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateSchema, CandidateReadSchema
from app.utils import constants


def create_candidate(body: CandidateSchema, db: Session) -> Candidate:
    """
    Creates a new candidate in the database.

    :param body: The candidate data, including name, email, and phone number.
    :param db: The SQLAlchemy database session used for database operations.
    :return: The newly created candidate object.

    :raises HTTPException: If the email or phone number is already in use,
                          or if there is a failure during candidate creation.
    """
    if db.query(Candidate).filter(Candidate.email == body.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=constants.EMAIL_ALREADY_INUSE_MESSAGE)

    if db.query(Candidate).filter(Candidate.phone == body.phone).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=constants.PHONE_NUMBER_ALREAY_INUSE_MESSAGE)

    candidate = Candidate(name=body.name, email=body.email, phone=body.phone)

    db.add(candidate)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=constants.CONDIDATE_CREATEION_FAILD)

    db.refresh(candidate)

    return candidate


def retrieve_candidate(candidate_id: str, db: Session) -> Candidate:
    """
    Retrieve a candidate from the database by their unique identifier.

    :param candidate_id: The unique identifier of the candidate to retrieve.
    :param db: The SQLAlchemy database session used for database operations.
    :return: The candidate object retrieved from the database, including
             associated skills and experience.

    :raises HTTPException: If no candidate is found with the provided ID, a
                          404 Not Found error is raised.
    """
    candidate = (db.query(Candidate).options(joinedload(Candidate.skills), joinedload(Candidate.experience))
                 .filter(Candidate.id == candidate_id).first())

    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found.")

    return candidate


def list_candidates(db: Session, params: Params) -> Page[CandidateReadSchema]:
    """
    Retrieve a paginated list of candidates from the database.

    :param db: The SQLAlchemy database session used for database operations.
    :param params: The parameters for pagination, including page number and page size.
    :return: A paginated list of candidates, including their details.

    :raises HTTPException: If there is an issue with retrieving the candidates.
    """
    return paginate(db.query(Candidate).all(), params=params)


def filter_candidates(db: Session, params: Params,
                      candidate_filter: CandidateFilter) -> Page[CandidateReadSchema]:
    """
     Retrieve a paginated list of candidates based on specified filters.

     :param db: The SQLAlchemy database session used for database operations.
     :param params: The parameters for pagination, including page number and page size.
     :param candidate_filter: The filter criteria to apply to the candidate query.
     :return: A paginated list of candidates that match the specified filters.

     :raises HTTPException: If there is an issue with filtering the candidates.
     """
    query = candidate_filter.filter(query=db.query(Candidate))
    return paginate(query.all(), params=params)


def delete_candidate(candidate_id: str, db: Session) -> None:
    """
    Delete a candidate from the database by their unique identifier.

    :param candidate_id: The unique identifier of the candidate to delete.
    :param db: The SQLAlchemy database session used for database operations.
    :return: None

    :raises HTTPException: If no candidate is found with the provided ID, a
                          404 Not Found error is raised.
    """
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found.")
    db.delete(candidate)

    db.commit()

    return {'message': 'candidate deleted.'}


def generate_candidates_report(db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Initiate the generation of a candidates report in CSV format.

    This function triggers an asynchronous task to generate a CSV file
    containing candidate information.

    :param db: The SQLAlchemy database session used for database operations.
                Defaults to the database session provided by FastAPI's dependency injection.
    :return: A message indicating that the report generation has been initiated.

    :raises HTTPException: If there is an issue with starting the report generation.
    """
    generate_candidates_csv_file.delay()

    return {'message': 'Generating report...'}
