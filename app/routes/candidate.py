from fastapi import APIRouter, Depends
from fastapi_filter.base.filter import FilterDepends
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from app.filters.candidate import CandidateFilter
from app.db.database import get_db
from app.filters.candidate import CandidateFilter
from app.models import Candidate
from app.schemas.condidate import CandidateSchema
from app.services import candidate


router = APIRouter(prefix="/candidates")


@router.get(path="/")
def list(db: Session = Depends(get_db), params:Params=Depends()):
    return candidate.list_candidates(db=db, params=params)


@router.post(path="/")
def create(body: CandidateSchema, db: Session = Depends(get_db)):
    return candidate.create(body=body, db=db)


@router.get(path="/{candidate_id}")
def retrieve(candidate_id: str, db: Session = Depends(get_db)):
    return candidate.retrieve(candidate_id=candidate_id, db=db)


@router.delete(path="/{candidate_id}")
def delete(candidate_id: str, db: Session = Depends(get_db)):
    return candidate.delete(candidate_id=candidate_id, db=db)


@router.get(path="/all/")
def filter_candidates(db: Session = Depends(get_db), params:Params=Depends(),  candidate_filter=FilterDepends(CandidateFilter)):
    return candidate.filter_candidates(db=db, params=params, candidate_filter=candidate_filter)