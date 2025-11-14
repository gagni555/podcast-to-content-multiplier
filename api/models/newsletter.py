from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.database import Base


class Newsletter(Base):
    __tablename__ = "newsletters"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    subject = Column(String, nullable=False)  # Email subject line
    html_content = Column(Text, nullable=False)  # HTML email content
    plain_text = Column(Text, nullable=False)  # Plain text version
    variant = Column(String, default="default")  # For A/B testing
    status = Column(String, default="draft")  # draft, sent, scheduled, failed
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())