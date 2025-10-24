from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateOut

router = APIRouter()


@router.post("/", response_model=CandidateOut)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.get("/", response_model=List[CandidateOut])
def list_candidates(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(10, le=100),
):
    return db.query(Candidate).offset(skip).limit(limit).all()


@router.put("/{candidate_id}", response_model=CandidateOut)
def update_candidate(
    candidate_id: int, candidate: CandidateCreate, db: Session = Depends(get_db)
):
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Candidate not found")

    # Update fields
    for key, value in candidate.dict().items():
        setattr(db_candidate, key, value)

    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate
