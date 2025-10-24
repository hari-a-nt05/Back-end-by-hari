from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.auth import get_current_user  # Assuming you have this dependency
from app.schemas.candidate import Candidate as CandidateSchema

router = APIRouter()

INDEED_API_URL = "https://api.indeed.com/v2/employer/jobs"  # Example endpoint
INDEED_API_KEY = "YOUR_INDEED_API_KEY"  # Replace with your actual key


class IndeedCandidateOut(BaseModel):
    candidate_id: str
    name: str
    email: str
    resume_url: str | None = None
    applied_at: str | None = None


class JobPostOut(BaseModel):
    job_id: str
    title: str
    location: str
    description: str
    posted_at: str


@router.get("/indeed/jobs/{job_id}/candidates", response_model=List[IndeedCandidateOut])
def get_candidates_for_job(job_id: str, user=Depends(get_current_user)):
    INDEED_CANDIDATES_API_URL = f"https://api.indeed.com/v2/jobs/{job_id}/candidates"
    headers = {"Authorization": f"Bearer {INDEED_API_KEY}"}
    response = requests.get(INDEED_CANDIDATES_API_URL, headers=headers)
    if response.status_code != 200:
        raise HTTPException(
            status_code=502, detail="Failed to fetch candidates from Indeed"
        )
    candidates = response.json().get("candidates", [])
    return [
        IndeedCandidateOut(
            candidate_id=c.get("id"),
            name=c.get("name"),
            email=c.get("email"),
            resume_url=c.get("resume_url"),
            applied_at=c.get("applied_at"),
        )
        for c in candidates
    ]


@router.get("/indeed/jobs/{employer_id}", response_model=List[JobPostOut])
def get_indeed_jobs(employer_id: str, user=Depends(get_current_user)):
    headers = {"Authorization": f"Bearer {INDEED_API_KEY}"}
    params = {"employer_id": employer_id}
    response = requests.get(INDEED_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch jobs from Indeed")
    jobs = response.json().get("jobs", [])
    return [
        JobPostOut(
            job_id=job.get("id"),
            title=job.get("title"),
            location=job.get("location"),
            description=job.get("description"),
            posted_at=job.get("posted_at"),
        )
        for job in jobs
    ]
