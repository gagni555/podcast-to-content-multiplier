from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/podcast_multiplier_dev")
    
    # Authentication
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-here-make-it-long-and-random")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # AWS S3
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "podcast-audio-files")
    s3_region: str = os.getenv("S3_REGION", "us-east-1")
    
    # AI Services
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Transcription Service
    assemblyai_api_key: Optional[str] = os.getenv("ASSEMBLYAI_API_KEY")
    
    # Redis (for Celery)
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Application
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "800"))
    
    # File upload limits
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "500"))
    max_audio_duration_seconds: int = int(os.getenv("MAX_AUDIO_DURATION_SECONDS", "14400"))  # 4 hours
    
    # Content generation
    default_blog_length: int = int(os.getenv("DEFAULT_BLOG_LENGTH", "200"))
    
    class Config:
        env_file = ".env"


settings = Settings()