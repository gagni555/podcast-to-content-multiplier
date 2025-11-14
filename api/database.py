from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database URL - using environment variable or default for development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/podcast_multiplier_dev")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()