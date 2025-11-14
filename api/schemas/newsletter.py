from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsletterBase(BaseModel):
    episode_id: int
    subject: str
    html_content: str
    plain_text: str
    variant: Optional[str] = "default"  # For A/B testing
    status: Optional[str] = "draft"
    scheduled_at: Optional[datetime] = None


class NewsletterCreate(NewsletterBase):
    class Config:
        from_attributes = True


class NewsletterUpdate(BaseModel):
    subject: Optional[str] = None
    html_content: Optional[str] = None
    plain_text: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Newsletter(NewsletterBase):
    id: int
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True