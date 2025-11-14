from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.database import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    text = Column(Text, nullable=False)  # Full transcript text
    segments_json = Column(String, nullable=True)  # JSON string of segments with timestamps
    speakers_json = Column(String, nullable=True)  # JSON string of speaker identification
    word_count = Column(Integer)  # Total word count
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())