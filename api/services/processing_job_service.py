from sqlalchemy.orm import Session
from typing import Optional
from api.models import ProcessingJob, Episode
from api.schemas import ProcessingJobCreate


def create_processing_job(db: Session, job: ProcessingJobCreate):
    """
    Create a new processing job
    """
    db_job = ProcessingJob(
        episode_id=job.episode_id,
        job_type=job.job_type,
        status=job.status,
        progress=job.progress,
        error_log=job.error_log
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return db_job


def get_processing_job(db: Session, job_id: int):
    """
    Get a processing job by ID
    """
    return db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()


def update_processing_job_status(db: Session, job_id: int, status: str, progress: Optional[int] = None, error_log: Optional[str] = None):
    """
    Update the status of a processing job
    """
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if job:
        job.status = status
        if progress is not None:
            job.progress = progress
        if error_log is not None:
            job.error_log = error_log
        db.commit()
        db.refresh(job)
    return job


def get_episode_processing_jobs(db: Session, episode_id: int):
    """
    Get all processing jobs for an episode
    """
    return db.query(ProcessingJob).filter(ProcessingJob.episode_id == episode_id).all()