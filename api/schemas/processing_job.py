from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProcessingJobBase(BaseModel):
    episode_id: int
    job_type: str  # transcription, blog, social, newsletter, all
    status: Optional[str] = "pending"
    progress: Optional[int] = 0  # 0-100 percentage
    error_log: Optional[str] = None


class ProcessingJobCreate(ProcessingJobBase):
    class Config:
        from_attributes = True


class ProcessingJob(ProcessingJobBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True