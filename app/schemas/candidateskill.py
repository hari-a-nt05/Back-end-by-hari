from pydantic import BaseModel


class CandidateSkillBase(BaseModel):
    skill_name: str
    score: int


class CandidateSkillCreate(CandidateSkillBase):
    candidate_id: int


class CandidateSkillOut(CandidateSkillBase):
    id: int
    candidate_id: int
