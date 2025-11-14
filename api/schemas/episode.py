from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EpisodeBase(BaseModel):
    title: str
    audio_url: str
    duration: Optional[int] = None
    file_size: Optional[int] = None
    file_format: Optional[str] = None
    generate_blog: Optional[bool] = True
    generate_social: Optional[bool] = True
    generate_newsletter: Optional[bool] = True
    generate_show_notes: Optional[bool] = True
    generate_quote_graphics: Optional[bool] = True


class EpisodeCreate(EpisodeBase):
    user_id: int
    
    class Config:
        from_attributes = True


class EpisodeUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    generate_blog: Optional[bool] = None
    generate_social: Optional[bool] = None
    generate_newsletter: Optional[bool] = None
    generate_show_notes: Optional[bool] = None
    generate_quote_graphics: Optional[bool] = None
    
    class Config:
        from_attributes = True


class Episode(EpisodeBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True