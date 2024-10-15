from fastapi import APIRouter, Depends, status
from fastapi_filter.base.filter import FilterDepends
from fastapi_pagination import Params, Page
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.filters.candidate import CandidateFilter
from app.schemas.candidate import CandidateSchema, CandidateReadSchema
from app.services import candidate
from app.utils import authentication

router = APIRouter(
    prefix="/candidates",
    tags=["Candidate"],
    dependencies=[Depends(authentication.get_current_user)],
)


@router.get(
    path="/", response_model=Page[CandidateReadSchema], status_code=status.HTTP_200_OK
)
def list_candidates(
    db: Session = Depends(get_db), params: Params = Depends()
) -> Page[CandidateReadSchema]:
    return candidate.list_candidates(db=db, params=params)


@router.post(
    path="/", response_model=CandidateReadSchema, status_code=status.HTTP_201_CREATED
)
def create_candidate(body: CandidateSchema, db: Session = Depends(get_db)):
    return candidate.create_candidate(body=body, db=db)


@router.get(
    path="/{candidate_id}",
    response_model=CandidateReadSchema,
    status_code=status.HTTP_200_OK,
)
def retrieve_candidate(candidate_id: str, db: Session = Depends(get_db)):
    return candidate.retrieve_candidate(candidate_id=candidate_id, db=db)


@router.delete(path="/{candidate_id}", status_code=status.HTTP_200_OK)
def delete_candidate(candidate_id: str, db: Session = Depends(get_db)):
    return candidate.delete_candidate(candidate_id=candidate_id, db=db)


@router.get(
    path="/all/",
    response_model=Page[CandidateReadSchema],
    status_code=status.HTTP_200_OK,
)
def filter_candidates(
    db: Session = Depends(get_db),
    params: Params = Depends(),
    candidate_filter=FilterDepends(CandidateFilter),
):
    return candidate.filter_candidates(
        db=db, params=params, candidate_filter=candidate_filter
    )


@router.get(path="/generate-report/", status_code=status.HTTP_202_ACCEPTED)
def generate_candidates_report(db: Session = Depends(get_db)):
    return candidate.generate_candidates_report(db=db)
