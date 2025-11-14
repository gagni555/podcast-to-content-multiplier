from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    subscription_tier = Column(String, default="free")  # free, starter, professional, agency
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Brand configuration (stored as JSON)
    brand_config = Column(String, nullable=True)  # JSON string for brand settings