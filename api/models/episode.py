from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from api.database import Base


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    audio_url = Column(String, nullable=False)  # URL to S3 or other storage
    duration = Column(Integer)  # Duration in seconds
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    file_size = Column(Integer)  # Size in bytes
    file_format = Column(String)  # MP3, WAV, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Processing options
    generate_blog = Column(Boolean, default=True)
    generate_social = Column(Boolean, default=True)
    generate_newsletter = Column(Boolean, default=True)
    generate_show_notes = Column(Boolean, default=True)
    generate_quote_graphics = Column(Boolean, default=True)