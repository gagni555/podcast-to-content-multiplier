from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.database import Base


class SocialThread(Base):
    __tablename__ = "social_threads"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    platform = Column(String, nullable=False)  # twitter, linkedin, instagram, facebook
    thread_json = Column(String, nullable=False)  # JSON string containing the thread structure
    status = Column(String, default="draft")  # draft, published, scheduled, failed
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())