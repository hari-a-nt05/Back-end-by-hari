from datetime import datetime
from typing import Optional
from uuid import UUID

from enum import Enum
from pydantic import BaseModel, EmailStr


class VisaType(str, Enum):
    h1b = "h1b"
    l1 = "l1"
    f1 = "f1"
    other = "other"


class CandidateBase(BaseModel):
    job_post_id: int
    name: str
    current_location: str
    email: EmailStr
    contact_number: str
    slot_availability: datetime
    rate_card_hourly: float
    experience_years: float
    visa_type: VisaType
    willing_to_relocate: bool
    overall_gpt_score: float
    notice_period_days: int
    cv_file_url: str
    remarks: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateOut(CandidateBase):
    id: int
    created_at: datetime
