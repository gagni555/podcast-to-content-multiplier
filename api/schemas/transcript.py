from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TranscriptBase(BaseModel):
    episode_id: int
    text: str
    segments_json: Optional[str] = None
    speakers_json: Optional[str] = None
    word_count: Optional[int] = None


class TranscriptCreate(TranscriptBase):
    class Config:
        from_attributes = True


class Transcript(TranscriptBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True