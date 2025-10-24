import uuid

import enum
from sqlalchemy import JSON, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.utils.helper import get_current_time


class EmploymentType(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"


class JobPost(Base):
    __tablename__ = "job_posts"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    company_intro = Column(Text)
    position = Column(String)
    location = Column(String)
    employment_type = Column(Enum(EmploymentType))
    department = Column(String)
    position_summary = Column(Text)
    key_responsibilities = Column(JSON)
    required_qualifications = Column(JSON)
    preferred_qualifications = Column(JSON)
    addons = Column(JSON, nullable=True)
    why_join_us = Column(Text)
    created_at = Column(DateTime, default=get_current_time())
    candidates = relationship("Candidate", back_populates="job_post")
