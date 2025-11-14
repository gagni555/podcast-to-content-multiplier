from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SocialThreadBase(BaseModel):
    episode_id: int
    platform: str  # twitter, linkedin, instagram, facebook
    thread_json: str  # JSON string containing the thread structure
    status: Optional[str] = "draft"
    scheduled_at: Optional[datetime] = None


class SocialThreadCreate(SocialThreadBase):
    class Config:
        from_attributes = True


class SocialThreadUpdate(BaseModel):
    thread_json: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SocialThread(SocialThreadBase):
    id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True