from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.jobpost import JobPost
from app.schemas.jobpost import JobPostCreate, JobPostOut

router = APIRouter()


@router.post("/", response_model=JobPostOut)
def create_job_post(job_post: JobPostCreate, db: Session = Depends(get_db)):
    db_job_post = JobPost(**job_post.dict())
    db.add(db_job_post)
    db.commit()
    db.refresh(db_job_post)
    return db_job_post


@router.get("/", response_model=List[JobPostOut])
def list_job_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(10, le=100),
):
    return db.query(JobPost).offset(skip).limit(limit).all()


@router.put("/{jobpost_id}", response_model=JobPostOut)
def update_job_post(
    jobpost_id: int, job_post: JobPostCreate, db: Session = Depends(get_db)
):
    db_job_post = db.query(JobPost).filter(JobPost.id == jobpost_id).first()
    if not db_job_post:
        raise HTTPException(status_code=404, detail="Job post not found")

    for key, value in job_post.dict().items():
        setattr(db_job_post, key, value)

    db.add(db_job_post)
    db.commit()
    db.refresh(db_job_post)
    return db_job_post
