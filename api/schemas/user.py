from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import json


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    subscription_tier: Optional[str] = "free"  # free, starter, professional, agency
    brand_config: Optional[str] = None  # JSON string for brand settings


class UserCreate(UserBase):
    password: str
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    subscription_tier: Optional[str] = None
    brand_config: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True