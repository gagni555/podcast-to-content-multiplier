from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.database import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)  # URL-friendly version of title
    content = Column(Text, nullable=False)  # HTML content
    excerpt = Column(Text)  # Short description
    word_count = Column(Integer)  # Total word count
    seo_title = Column(String)  # SEO-optimized title
    seo_description = Column(String)  # Meta description for SEO
    seo_keywords = Column(String)  # Comma-separated keywords
    status = Column(String, default="draft")  # draft, published, scheduled
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())