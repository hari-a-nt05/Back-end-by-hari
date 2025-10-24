from datetime import datetime
from typing import Any, Optional

from enum import Enum
from pydantic import BaseModel


class EmploymentType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"


class JobPostBase(BaseModel):
    title: str
    company_intro: str
    position: str
    location: str
    employment_type: EmploymentType
    department: str
    position_summary: str
    key_responsibilities: Any
    required_qualifications: Any
    preferred_qualifications: Any
    addons: Optional[Any] = None
    why_join_us: str


class JobPostCreate(JobPostBase):
    pass


class JobPostOut(JobPostBase):
    id: int
    created_at: datetime
