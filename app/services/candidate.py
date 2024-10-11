from fastapi import HTTPException, status
from fastapi_pagination import Params, paginate
from sqlalchemy.orm import Session, joinedload

from app.filters.candidate import CandidateFilter
from app.models.candidate import Candidate
from app.schemas.condidate import CandidateSchema, CandidateReadSchema
from app.utils import constants


def create(body: CandidateSchema, db: Session):
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

    return {'candidate': candidate}


def retrieve(candidate_id: str, db: Session):
    candidate = (db.query(Candidate).options(joinedload(Candidate.skills), joinedload(Candidate.experience))
                 .filter(Candidate.id == candidate_id).first())

    if not candidate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate not found.")

    return {'candidate': candidate}


def list_candidates(db: Session, params: Params):
    query = db.query(Candidate).options(
        joinedload(Candidate.skills),
        joinedload(Candidate.experience)
    ).order_by(Candidate.id).all()
    return paginate([CandidateReadSchema.model_validate(candidate) for candidate in query], params=params)


def filter_candidates(db: Session, params: Params,
                      candidate_filter: CandidateFilter):
    query = db.query(Candidate).options(
        joinedload(Candidate.skills),
        joinedload(Candidate.experience)
    ).order_by(Candidate.id)

    query = candidate_filter.filter(query=query)
    return paginate([CandidateReadSchema.model_validate(candidate) for candidate in query], params=params)


def delete(candidate_id: str, db: Session):
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate not found.")
    db.delete(candidate)

    db.commit()

    return {'message': 'candidate deleted.'}
