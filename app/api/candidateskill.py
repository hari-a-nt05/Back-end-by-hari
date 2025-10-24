from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidateskill import CandidateSkill
from app.schemas.candidateskill import CandidateSkillCreate, CandidateSkillOut

router = APIRouter()


@router.post("/", response_model=CandidateSkillOut)
def create_candidate_skill(skill: CandidateSkillCreate, db: Session = Depends(get_db)):
    db_skill = CandidateSkill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.get("/", response_model=List[CandidateSkillOut])
def list_candidate_skills(db: Session = Depends(get_db)):
    return db.query(CandidateSkill).all()
