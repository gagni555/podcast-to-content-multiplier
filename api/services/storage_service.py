import os
import uuid
from typing import Optional
from config import settings


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename by adding a UUID prefix
    """
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    return unique_filename


def validate_file_type(content_type: str) -> bool:
    """
    Validate if the file type is allowed
    """
    allowed_types = ["audio/mpeg", "audio/wav", "audio/x-m4a", "audio/flac"]
    return content_type in allowed_types


def validate_file_size(file_size: int) -> bool:
    """
    Validate if the file size is within the allowed limit
    """
    max_size = settings.max_file_size_mb * 1024 * 1024  # Convert MB to bytes
    return file_size <= max_size


def get_file_size_limit_mb() -> int:
    """
    Get the maximum file size limit in MB
    """
    return settings.max_file_size_mb


def get_audio_duration_limit_seconds() -> int:
    """
    Get the maximum audio duration limit in seconds
    """
    return settings.max_audio_duration_seconds