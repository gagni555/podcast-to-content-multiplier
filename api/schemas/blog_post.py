from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlogPostBase(BaseModel):
    episode_id: int
    title: str
    content: str
    excerpt: Optional[str] = None
    word_count: Optional[int] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    status: Optional[str] = "draft"


class BlogPostCreate(BlogPostBase):
    class Config:
        from_attributes = True


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    
    class Config:
        from_attributes = True


class BlogPost(BlogPostBase):
    id: int
    slug: str
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True