import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.utils.helper import get_current_time


class VisaType(str, enum.Enum):
    h1b = "h1b"
    l1 = "l1"
    f1 = "f1"
    other = "other"


class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    job_post_id = Column(Integer, ForeignKey("job_posts.id"))
    name = Column(String)
    current_location = Column(String)
    email = Column(String, index=True)
    contact_number = Column(String)
    slot_availability = Column(DateTime)
    rate_card_hourly = Column(Numeric)
    experience_years = Column(Numeric)
    visa_type = Column(Enum(VisaType))
    willing_to_relocate = Column(Boolean)
    overall_gpt_score = Column(Numeric)
    notice_period_days = Column(Integer)
    cv_file_url = Column(String)
    remarks = Column(Text)
    created_at = Column(DateTime, default=get_current_time())
    job_post = relationship("JobPost", back_populates="candidates")
    skills = relationship("CandidateSkill", back_populates="candidate")
