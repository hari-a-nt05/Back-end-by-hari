from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String)
    score = Column(Integer)
    candidate_id = Column(ForeignKey("candidates.id"))
    candidate = relationship("Candidate", back_populates="skills")
